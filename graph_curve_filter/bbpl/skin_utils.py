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
from .. import bbpl

def save_defoms_bones(armature):
    """
    Save the deform flag for each bone in the armature.
    Returns a list of bone names and their deform flags.
    """
    saved_bones = []
    for bone in armature.data.bones:
        saved_bones.append([bone.name, bone.use_deform])
    return saved_bones


def reset_deform_bones(armature, saved_bones):
    """
    Reset the deform flags for each bone in the armature using the saved data.
    """
    for bones in saved_bones:
        armature.data.bones[bones[0]].use_deform = bones[1]


def set_all_bones_deforms(armature, use_deform):
    """
    Set the deform flag for all bones in the armature.
    """
    for bone in armature.data.bones:
        bone.use_deform = use_deform


def set_bones_deforms(armature, bone_name_list, use_deform):
    """
    Set the deform flag for the specified bones in the armature.
    """
    bone_list = []
    for bone_name in bone_name_list:
        bone_list.append(armature.data.bones[bone_name])
    for bone in bone_list:
        bone.use_deform = use_deform


def remove_vertex_groups(obj):
    """
    Remove all vertex groups from the object.
    """
    for vertex_group in obj.vertex_groups:
        obj.vertex_groups.remove(vertex_group)


def copy_rig_group(obj, source):
    """
    Copy the rigging weights from the source object to the target object.
    """
    bbpl.utils.mode_set_on_target(obj, "OBJECT")

    mod_name = "MAR_RigWeightTransfer"

    for old_mod in obj.modifiers:
        if old_mod.name == mod_name:
            obj.modifiers.remove(old_mod)

    remove_vertex_groups(obj)

    mod = obj.modifiers.new(name=mod_name, type='DATA_TRANSFER')
    while obj.modifiers[0].name != mod_name:
        bpy.ops.object.modifier_move_up(modifier=mod_name)

    mod.object = source
    mod.use_vert_data = True
    mod.data_types_verts = {'VGROUP_WEIGHTS'}
    bpy.ops.object.datalayout_transfer(modifier=mod_name, data_type="VGROUP_WEIGHTS")
    bpy.ops.object.modifier_apply(modifier=mod_name)


def apply_auto_rig_parent(armature, target_objects, parent_type='ARMATURE_AUTO', white_list_bones=[], black_list_bones=[]):
    """
    Apply an automatic rig parent to the target object using the armature.
    Optionally, specify a white list or black list of bones to control the deform flag.
    """

    save_defom = save_defoms_bones(armature)

    if len(white_list_bones) > 0:
        set_all_bones_deforms(armature, False)

    set_bones_deforms(armature, white_list_bones, True)
    set_bones_deforms(armature, black_list_bones, False)

    for obj in target_objects:
        for modifier in obj.modifiers:
            if modifier.type == "ARMATURE":
                obj.modifiers.remove(modifier)
        remove_vertex_groups(obj)
    
    all_objs = []
    all_objs.append(armature)
    all_objs.extend(target_objects)
    if bpy.app.version >= (4, 0, 0):
        with bpy.context.temp_override(active_object=armature, object=armature, selected_objects=all_objs, selected_editable_objects=all_objs):
            bpy.ops.object.parent_set(type=parent_type)

    else:
        override_context = bpy.context.copy()
        override_context['active_object'] = armature
        override_context['object'] = armature
        override_context['selected_objects'] = all_objs
        bpy.ops.object.parent_set(override_context, type=parent_type)


    reset_deform_bones(armature, save_defom)