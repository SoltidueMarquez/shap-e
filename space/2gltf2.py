# 
# The MIT License (MIT)
#
# Copyright (c) since 2017 UX3D GmbH
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 

#
# Imports
#

import bpy
import os
import sys

#
# Globals
#

#
# Functions
#

current_directory = os.getcwd()

force_continue = True

for current_argument in sys.argv:

    if force_continue:
        if current_argument == '--':
            force_continue = False
        continue

    #

    root, current_extension = os.path.splitext(current_argument)
    current_basename = os.path.basename(root)

    if current_extension != ".abc" and current_extension != ".blend" and current_extension != ".dae" and current_extension != ".fbx" and current_extension != ".obj" and current_extension != ".ply" and current_extension != ".stl" and current_extension != ".usd" and current_extension != ".usda" and current_extension != ".usdc" and current_extension != ".wrl" and current_extension != ".x3d":
        continue

    bpy.ops.wm.read_factory_settings(use_empty=True)
    print("Converting: '" + current_argument + "'")

    #

    if current_extension == ".abc":
        bpy.ops.wm.alembic_import(filepath=current_argument)    

    if current_extension == ".blend":
        bpy.ops.wm.open_mainfile(filepath=current_argument)

    if current_extension == ".dae":
        bpy.ops.wm.collada_import(filepath=current_argument)    

    if current_extension == ".fbx":
        bpy.ops.import_scene.fbx(filepath=current_argument)    

    if current_extension == ".obj":
        bpy.ops.import_scene.obj(filepath=current_argument)    

    if current_extension == ".ply":
        bpy.ops.import_mesh.ply(filepath=current_argument)    

    if current_extension == ".stl":
        bpy.ops.import_mesh.stl(filepath=current_argument)

    if current_extension == ".usd" or current_extension == ".usda" or current_extension == ".usdc":
        bpy.ops.wm.usd_import(filepath=current_argument)

    if current_extension == ".wrl" or current_extension == ".x3d":
        bpy.ops.import_scene.x3d(filepath=current_argument)

    #

    export_file = current_directory + "/" + current_basename + ".gltf"
    print("Writing: '" + export_file + "'")
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='EDIT')
    #bpy.ops.gpencil.layer_active(layer=0)
    #bpy.ops.gpencil.select_all(action='SELECT')
    print(bpy.data.meshes['mesh'].vertex_colors)
    print(bpy.context.mode)
    #bpy.ops.mesh.colors_reverse()
    #bpy.ops.mesh.colors_rotate(use_ccw=False)
    #bpy.ops.gpencil.vertex_color_invert(mode='BOTH')
    #bpy.ops.gpencil.vertex_color_brightness_contrast(mode='FILL', brightness=0.0, contrast=0.0)
    #bpy.ops.object.light_add(type="POINT", radius=1000, align="WORLD",location=(-50, 100, 100))
    bpy.ops.export_scene.gltf(filepath=export_file, export_lights=True, export_materials="EXPORT", export_colors=True, export_format="GLTF_EMBEDDED")
