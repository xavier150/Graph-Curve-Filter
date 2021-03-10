# ====================== BEGIN GPL LICENSE BLOCK ============================
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#
# ======================= END GPL LICENSE BLOCK =============================


import bpy
import fnmatch
import mathutils
import math
import time
import sys

if "bpy" in locals():
    import importlib
    if "gcf_basics" in locals():
        importlib.reload(gcf_basics)
from . import gcf_basics
from .gcf_basics import *


class SavedObject():

    def __init__(self, obj):
        if obj:
            self.name = obj.name
            self.select = obj.select_get()
            self.hide = obj.hide_get()
            self.hide_select = obj.hide_select
            self.hide_viewport = obj.hide_viewport


class SavedBones():

    def __init__(self, bone):
        if bone:
            self.name = bone.name
            self.select = bone.select
            self.hide = bone.hide


class SavedCollection():

    def __init__(self, col):
        if col:
            self.name = col.name
            self.hide_select = col.hide_select
            self.hide_viewport = col.hide_viewport


class SavedViewLayerChildren():

    def __init__(self, vlayer, childCol):
        if childCol:
            self.vlayer_name = vlayer.name
            self.name = childCol.name
            self.exclude = childCol.exclude
            self.hide_viewport = childCol.hide_viewport


class UserSceneSave():

    def __init__(self):

        # Select
        self.user_active = None
        self.user_active_name = None
        self.user_bone_active = None
        self.user_bone_active_name = None
        self.user_selected = []

        # Stats
        self.user_mode = None
        self.use_simplify = False

        # Data
        self.objects = []
        self.object_bones = []
        self.collections = []
        self.view_layers_children = []
        self.action_names = []
        self.collection_names = []

    def SaveCurrentScene(self):
        # Save data (This can take time)

        c = bpy.context
        # Select
        self.user_active = c.active_object  # Save current active object
        if self.user_active:
            self.user_active_name = self.user_active.name
        self.user_selected = c.selected_objects  # Save current selected objects

        # Stats
        if self.user_active:
            if bpy.ops.object.mode_set.poll():
                self.user_mode = self.user_active.mode  # Save current mode
        self.use_simplify = bpy.context.scene.render.use_simplify

        # Data
        for obj in bpy.data.objects:
            self.objects.append(SavedObject(obj))
        for col in bpy.data.collections:
            self.collections.append(SavedCollection(col))
        for vlayer in c.scene.view_layers:
            for childCol in vlayer.layer_collection.children:
                self.view_layers_children.append(SavedViewLayerChildren(vlayer, childCol))
        for action in bpy.data.actions:
            self.action_names.append(action.name)
        for collection in bpy.data.collections:
            self.collection_names.append(collection.name)

        # Data for armature
        if self.user_active:
            if self.user_active.type == "ARMATURE":
                if self.user_active.data.bones.active:
                    self.user_bone_active = self.user_active.data.bones.active
                    self.user_bone_active_name = self.user_active.data.bones.active.name
                for bone in self.user_active.data.bones:
                    self.object_bones.append(SavedBones(bone))

    def ResetSelectByRef(self):
        SafeModeSet("OBJECT", bpy.ops.object)
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.data.objects:  # Resets previous selected object if still exist
            if obj in self.user_selected:
                obj.select_set(True)

        bpy.context.view_layer.objects.active = self.user_active

        self.ResetModeAtSave()
        self.ResetBonesSelectByName()

    def ResetSelectByName(self):
        SafeModeSet("OBJECT", bpy.ops.object)
        bpy.ops.object.select_all(action='DESELECT')
        for obj in self.objects:  # Resets previous selected object if still exist
            if obj.select:
                if obj.name in bpy.data.objects:
                    if obj.name in bpy.context.view_layer.objects:
                        bpy.data.objects[obj.name].select_set(True)

        if self.user_active_name:
            if self.user_active_name in bpy.data.objects:
                if self.user_active_name in bpy.context.view_layer.objects:
                    bpy.context.view_layer.objects.active = bpy.data.objects[self.user_active_name]

        self.ResetModeAtSave()
        self.ResetBonesSelectByName()

    def ResetBonesSelectByName(self):
        # Work only in pose mode!
        if len(self.object_bones) > 0:
            if self.user_active:
                if bpy.ops.object.mode_set.poll():
                    if self.user_active.mode == "POSE":
                        bpy.ops.pose.select_all(action='DESELECT')
                        for bone in self.object_bones:
                            if bone.select:
                                if bone.name in self.user_active.data.bones:
                                    self.user_active.data.bones[bone.name].select = True

                        if self.user_bone_active_name is not None:
                            if self.user_bone_active_name in self.user_active.data.bones:
                                new_active = self.user_active.data.bones[self.user_bone_active_name]
                                self.user_active.data.bones.active = new_active

    def ResetModeAtSave(self):
        if self.user_mode:
            if bpy.ops.object:
                SafeModeSet(self.user_mode, bpy.ops.object)

    def ResetSceneAtSave(self):
        scene = bpy.context.scene
        self.ResetModeAtSave()

        bpy.context.scene.render.use_simplify = self.use_simplify

        # Reset hide and select (bpy.data.objects)
        for obj in self.objects:
            if obj.name in bpy.data.objects:
                if bpy.data.objects[obj.name].hide_select != obj.hide_select:
                    bpy.data.objects[obj.name].hide_select = obj.hide_select
                if bpy.data.objects[obj.name].hide_viewport != obj.hide_viewport:
                    bpy.data.objects[obj.name].hide_viewport = obj.hide_viewport
                if bpy.data.objects[obj.name].hide_get() != obj.hide:
                    bpy.data.objects[obj.name].hide_set(obj.hide)

            else:
                print("/!\\ "+obj.name+" not found in bpy.data.objects")

        # Reset hide and select (bpy.data.collections)
        for col in self.collections:
            if col.name in bpy.data.collections:
                if bpy.data.collections[col.name].hide_select != col.hide_select:
                    bpy.data.collections[col.name].hide_select = col.hide_select
                if bpy.data.collections[col.name].hide_viewport != col.hide_viewport:
                    bpy.data.collections[col.name].hide_viewport = col.hide_viewport
            else:
                print("/!\\ "+col.name+" not found in bpy.data.collections")

        # Reset hide in and viewport (collections from view_layers)
        for childCol in self.view_layers_children:
            if childCol.vlayer_name in scene.view_layers:
                view_layer = scene.view_layers[childCol.vlayer_name]
                if childCol.name in view_layer.layer_collection.children:
                    layer_col_children = view_layer.layer_collection.children[childCol.name]

                    if layer_col_children.exclude != childCol.exclude:
                        layer_col_children.exclude = childCol.exclude
                    if layer_col_children.hide_viewport != childCol.hide_viewport:
                        layer_col_children.hide_viewport = childCol.hide_viewport


class AnimationManagment():
    def __init__(self):
        self.action = None
        self.action_extrapolation = None
        self.action_blend_type = None
        self.action_influence = None

    def SaveAnimationData(self, obj):
        self.action = obj.animation_data.action
        self.action_extrapolation = obj.animation_data.action_extrapolation
        self.action_blend_type = obj.animation_data.action_blend_type
        self.action_influence = obj.animation_data.action_influence

    def ClearAnimationData(self, obj):
        obj.animation_data_clear()

    def SetAnimationData(self, obj):
        obj.animation_data_create()
        obj.animation_data.action = self.action
        obj.animation_data.action_extrapolation = self.action_extrapolation
        obj.animation_data.action_blend_type = self.action_blend_type
        obj.animation_data.action_influence = self.action_influence


def SafeModeSet(target_mode='OBJECT', obj=None):
    if bpy.ops.object.mode_set.poll():
        if obj:
            if obj.mode != target_mode:
                bpy.ops.object.mode_set(mode=target_mode)
                return True

        else:
            bpy.ops.object.mode_set(mode=target_mode)
            return True

    return False


class CounterTimer():

    def __init__(self):
        self.start = time.perf_counter()

    def ResetTime(self):
        self.start = time.perf_counter()

    def GetTime(self):
        return time.perf_counter()-self.start


def update_progress(job_title, progress, time=None):

    length = 20  # modify this to change the length
    block = int(round(length*progress))
    msg = "\r{0}: [{1}] {2}%".format(
        job_title,
        "#"*block + "-"*(length-block),
        round(progress*100, 2))
    if progress >= 1:
        if time is not None:
            msg += " DONE IN " + str(round(time, 2)) + "s\r\n"
        else:
            msg += " DONE\r\n"
    sys.stdout.write(msg)
    sys.stdout.flush()


def RemoveUselessSpecificData(name, type):
    if type == "MESH":
        if name in bpy.data.meshes:
            oldData = bpy.data.meshes[name]
            if oldData.users == 0:
                bpy.data.meshes.remove(oldData)

    if type == "ARMATURE":
        if name in bpy.data.armatures:
            oldData = bpy.data.armatures[name]
            if oldData.users == 0:
                bpy.data.armatures.remove(oldData)


def CleanJoinSelect():
    view_layer = bpy.context.view_layer
    if len(bpy.context.selected_objects) > 1:
        if view_layer.objects.active is None:
            view_layer.objects.active = bpy.context.selected_objects[0]

        if bpy.ops.object.convert.poll():
            bpy.ops.object.join()


def CleanDeleteSelect():

    removed_objects = []
    oldDataToRemove = []
    for obj in bpy.context.selected_objects:
        removed_objects.append(obj.name)
        if obj.data is not None:
            oldDataToRemove.append([obj.data.name, obj.type])

    bpy.ops.object.delete()

    for data in oldDataToRemove:
        RemoveUselessSpecificData(data[0], data[1])

    return removed_objects


def CleanDeleteObjects(objs):

    objs = list(dict.fromkeys(objs))

    removed_objects = []
    for obj in objs:

        souldRemoveData = False
        if obj.data is not None:
            oldDataToRemove = obj.data.name
            oldDataTypeToRemove = obj.type
            souldRemoveData = True

        removed_objects.append(obj.name)
        bpy.data.objects.remove(obj)

        if souldRemoveData:
            RemoveUselessSpecificData(oldDataToRemove, oldDataTypeToRemove)

    return removed_objects


def GoToMeshEditMode():
    for obj in bpy.context.selected_objects:
        if obj.type == "MESH":
            bpy.context.view_layer.objects.active = obj
            SafeModeSet('EDIT')

            return True
    return False


def ApplyNeededModifierToSelect():

    SavedSelect = GetCurrentSelection()
    for obj in bpy.context.selected_objects:
        if obj.type == "MESH":
            SelectSpecificObject(obj)
            for mod in [m for m in obj.modifiers if m.type != 'ARMATURE']:
                if obj.data.shape_keys is None:
                    if obj.data.users > 1:
                        obj.data = obj.data.copy()
                    if bpy.ops.object.modifier_apply.poll():
                        bpy.ops.object.modifier_apply(modifier=mod.name)

    SetCurrentSelection(SavedSelect)


def ApplyExportTransform(obj):
    newMatrix = obj.matrix_world @ mathutils.Matrix.Translation((0, 0, 0))
    saveScale = obj.scale * 1

    # Ref
    # Moves object to the center of the scene for export
    if obj.MoveToCenterForExport:
        mat_trans = mathutils.Matrix.Translation((0, 0, 0))
        mat_rot = newMatrix.to_quaternion().to_matrix()
        newMatrix = mat_trans @ mat_rot.to_4x4()

    # Turn object to the center of the scene for export
    if obj.RotateToZeroForExport:
        mat_trans = mathutils.Matrix.Translation(newMatrix.to_translation())
        mat_rot = mathutils.Matrix.Rotation(0, 4, 'X')
        newMatrix = mat_trans @ mat_rot

    eul = obj.AdditionalRotationForExport
    loc = obj.AdditionalLocationForExport

    mat_rot = eul.to_matrix()
    mat_loc = mathutils.Matrix.Translation(loc)
    AddMat = mat_loc @ mat_rot.to_4x4()

    obj.matrix_world = newMatrix @ AddMat
    obj.scale = saveScale
