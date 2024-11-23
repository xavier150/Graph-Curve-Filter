# ====================== BEGIN GPL LICENSE BLOCK ============================
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.	 If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#
# ======================= END GPL LICENSE BLOCK =============================

# ----------------------------------------------
#  BBPL -> BleuRaven Blender Python Library
#  BleuRaven.fr
#  XavierLoux.com
# ----------------------------------------------

import bpy
from ... import __package__ as base_package

def get_package_name():
    # Before 4.2 __package__ will look like that: 
    # my_blender_addon.bbpl.__internal__

    # After 4.2 __package__ will look like that: 
    # bl_ext.user_default.my_blender_addon.bbpl.__internal__

    package_name = base_package.split(".")[-1]
    return package_name

def get_reduced_package_name():
    package_name = get_package_name()

    # blender-for-unrealengine -> bdfunr
    # unrealengine_assets_exporter -> unrassexp

    separators = ["-", "_", "."]
    for sep in separators:
        package_name = package_name.replace(sep, " ")
    parts = package_name.split()

    special_reductions = {
        "blender": "bd",
        "for": "f",
        "to": "t",
        "assets": "ass",
        "asset": "as",
    }

    reduced_parts = []
    for part in parts:
        reduced_part = special_reductions.get(part, part[:3])
        reduced_parts.append(reduced_part)

    reduced_name = ''.join(reduced_parts).lower()[:12] # Max length is 12
    return reduced_name

def get_operator_class_name(name):
    reduced_package_name = get_reduced_package_name()
    return f"BBPL_OT_{reduced_package_name}_{name}"

def get_data_operator_idname(name):
    reduced_package_name = get_reduced_package_name()
    return f"data.bbpl_{reduced_package_name}_{name}"

def get_object_operator_idname(name):
    reduced_package_name = get_reduced_package_name()
    return f"object.bbpl_{reduced_package_name}_{name}"

def get_scene_operator_idname(name):
    reduced_package_name = get_reduced_package_name()
    return f"scene.bbpl_{reduced_package_name}_{name}"