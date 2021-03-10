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

import os
import bpy
import addon_utils
import time

from . import gcf_basics
from .gcf_basics import *
from . import gcf_utils
from .gcf_utils import *
from . import gcf_ui_utils
from . import languages
from .languages import *


if "bpy" in locals():
    import importlib
    if "gcf_basics" in locals():
        importlib.reload(gcf_basics)
    if "gcf_utils" in locals():
        importlib.reload(gcf_utils)
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


class GCF_PT_GraphCurveFilter(bpy.types.Panel):
    # Graph Curve Filter panel

    bl_idname = "GCF_PT_GraphCurveFilter"
    bl_label = "Curbe Filter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Curbe Filter"

    class GCF_OT_OpenDocumentationPage(Operator):
        bl_label = "Documentation"
        bl_idname = "object.gcf_open_documentation_page"
        bl_description = "Clic for open documentation page on GitHub"

        def execute(self, context):
            os.system(
                "start \"\" " +
                "https://github.com/xavier150/Blender-Graph-Curbe-Filter"
                )
            return {'FINISHED'}

    def draw(self, contex):
        scene = bpy.context.scene
        obj = bpy.context.object
        addon_prefs = bpy.context.preferences.addons[__package__].preferences
        layout = self.layout

        version = "-1"
        for addon in addon_utils.modules():
            if addon.bl_info['name'] == "Graph Curbe Filter":
                version = addon.bl_info.get('version', (-1, -1, -1))

        credit_box = layout.box()
        credit_box.label(text=ti('intro')+' Version: '+str(version))
        credit_box.operator("object.gcf_open_documentation_page", icon="HELP")


classes = (
    GCF_PT_GraphCurveFilter,
    GCF_PT_GraphCurveFilter.GCF_OT_OpenDocumentationPage,
)


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)
