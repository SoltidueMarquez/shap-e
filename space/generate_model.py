import argparse
import os
import shutil
import torch

from shap_e.diffusion.sample import sample_latents
from shap_e.diffusion.gaussian_diffusion import diffusion_from_config
from shap_e.models.download import load_model, load_config
from shap_e.util.notebooks import decode_latent_mesh

# 设置命令行参数解析
def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate a 3D model from a text prompt")
    parser.add_argument(
        '--prompt',
        type=str,
        required=True,
        help="Text prompt to generate the model (e.g., 'a shark')"
    )
    return parser.parse_args()

# 清理文件夹内容
def clean_cache(folder_path):
    if os.path.exists(folder_path):
        try:
            # 删除文件夹内的所有内容
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)  # 删除文件
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)  # 删除子文件夹
            print(f"Cache folder '{folder_path}' cleaned successfully.")
        except Exception as e:
            print(f"Error while cleaning cache folder: {e}")
    else:
        print(f"Cache folder '{folder_path}' does not exist.")

# 解析命令行参数
args = parse_arguments()
prompt = args.prompt

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 加载模型
xm = load_model('transmitter', device=device)
model = load_model('text300M', device=device)

# 加载扩散模型
diffusion = diffusion_from_config({
    "schedule": "linear",    # 或 "cosine"，取决于你的需求
    "timesteps": 1024,       # 原始时间步数
    "respacing": "256"       # 新的时间步数（可以改为更少的步数，如 256）
})

# 设置采样参数
batch_size = 1
guidance_scale = 1.0  # 尝试降低该值

# 采样潜变量
latents = sample_latents(
    batch_size=batch_size,
    model=model,
    diffusion=diffusion,
    guidance_scale=guidance_scale,
    model_kwargs=dict(texts=[prompt] * batch_size),
    progress=True,
    clip_denoised=True,
    use_fp16=False,  # 尝试禁用 FP16
    use_karras=False,
    karras_steps=32,
    sigma_min=1e-3,
    sigma_max=160,
    s_churn=0,
)

# 解码潜变量为网格模型
for i, latent in enumerate(latents):
    t = decode_latent_mesh(xm, latent).tri_mesh()
    with open(f'mesh{i}.ply', 'wb') as f:
        t.write_ply(f)

print(f"3D model generated and saved as 'example_mesh_0.ply'")

# 清理缓存文件夹
cache_folder = "shap_e_model_cache"  # 替换为实际的缓存文件夹路径
clean_cache(cache_folder)
