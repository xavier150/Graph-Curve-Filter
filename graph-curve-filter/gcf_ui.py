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
    bl_space_type = "GRAPH_EDITOR"
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

    class GCF_OT_FilterSet(Operator):
        bl_label = "My Filter"
        bl_idname = "object.gcf_filter_set"
        bl_description = "Clic for filter"
        filter_name: StringProperty(default="None")
        use_filter_invert: BoolProperty(default=False)

        def execute(self, context):
            bpy.context.space_data.dopesheet.filter_text = self.filter_name
            bpy.context.space_data.dopesheet.use_filter_invert = self.use_filter_invert

            print(self.filter_name)
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

        def AddFilter(layout, filter_name: str, visual_text: str):
            new_filter = layout.operator("object.gcf_filter_set", text=visual_text)
            new_filter.filter_name = filter_name

        filter_group = layout.box()
        loc_filter = filter_group.row()
        AddFilter(loc_filter, "Location", "Loc")
        AddFilter(loc_filter, "X Location", "X")
        AddFilter(loc_filter, "Y Location", "Y")
        AddFilter(loc_filter, "Z Location", "Z")
        euler_filter = filter_group.row()
        AddFilter(euler_filter, "Euler", "Euler")
        AddFilter(euler_filter, "X Euler", "X")
        AddFilter(euler_filter, "Y Euler", "Y")
        AddFilter(euler_filter, "Z Euler", "Z")
        scale_filter = filter_group.row()
        AddFilter(scale_filter, "Scale", "Scale")
        AddFilter(scale_filter, "X Scale", "X")
        AddFilter(scale_filter, "Y Scale", "Y")
        AddFilter(scale_filter, "Z Scale", "Z")
        all_filter = filter_group.row()
        AddFilter(all_filter, "", "ALL")
        AddFilter(all_filter, "XOXOXOXOXOXOXO", "NONE")


classes = (
    GCF_PT_GraphCurveFilter,
    GCF_PT_GraphCurveFilter.GCF_OT_OpenDocumentationPage,
    GCF_PT_GraphCurveFilter.GCF_OT_FilterSet,
)


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)
