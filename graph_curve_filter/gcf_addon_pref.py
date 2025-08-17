# SPDX-FileCopyrightText: 2021-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Graph Curve Filter
#  https://github.com/xavier150/Graph-Curve-Filter
# ----------------------------------------------

import os
import bpy
import addon_utils

from . import gcf_basics
from .gcf_basics import *
from . import gcf_utils
from .gcf_utils import *
from . import gcf_ui_utils
from . import languages
from .languages import *


if "bpy" in locals():
    import importlib
    if "gcf_export_asset" in locals():
        importlib.reload(gcf_export_asset)
    if "gcf_write_text" in locals():
        importlib.reload(gcf_write_text)
    if "gcf_basics" in locals():
        importlib.reload(gcf_basics)
    if "gcf_utils" in locals():
        importlib.reload(gcf_utils)
    if "gcf_check_potential_error" in locals():
        importlib.reload(gcf_check_potential_error)
    if "gcf_ui_utils" in locals():
        importlib.reload(gcf_ui_utils)
    if "languages" in locals():
        importlib.reload(languages)


from bpy.props import (
        StringProperty,
        BoolProperty,
        EnumProperty,
        IntProperty,
        FloatProperty,
        FloatVectorProperty,
        PointerProperty,
        CollectionProperty,
        )

from bpy.types import (
        Operator,
        )


class GCF_AP_AddonPreferences(bpy.types.AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout


classes = (

)


def menu_func(self, context):
    layout = self.layout
    col = layout.column()
    col.separator(factor=1.0)
    col.operator(GCF_PT_CorrectAndImprov.GCF_OT_CorrectExtremUV.bl_idname)


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)

    bpy.types.VIEW3D_MT_uv_map.remove(menu_func)
