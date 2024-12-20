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
from . import bbpl

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

        # Extension details
        if bpy.app.version >= (4, 2, 0):
            version_str = 'Version '+ str(bbpl.blender_extension.extension_utils.get_package_version())
        else:
            version_str = 'Version '+ bbpl.blender_addon.addon_utils.get_addon_version_str("Unreal Engine Assets Exporter")

        credit_box = layout.box()
        credit_box.label(text=languages.ti('intro'))
        credit_box.label(text=version_str)
        bbpl.blender_layout.layout_doc_button.functions.add_doc_page_operator(
            layout = layout,
            url = "https://github.com/xavier150/Blender-For-UnrealEngine-Addons",
            text = "Open Github page",
            icon="HELP"
            )

        def AddFilter(layout, filter_name: str, visual_text: str, full_text: str):
            new_filter = layout.operator("object.gcf_filter_set", text=visual_text)
            new_filter.filter_name = filter_name

        filter_group_transform = layout.box()

        loc_filter = filter_group_transform.row()
        AddFilter(loc_filter, "Location", "Loc", "Location")
        AddFilter(loc_filter, "X Location", "X", "X Location")
        AddFilter(loc_filter, "Y Location", "Y", "Y Location")
        AddFilter(loc_filter, "Z Location", "Z", "Z Location")

        euler_filter = filter_group_transform.row()
        AddFilter(euler_filter, "Euler", "Euler", "Euler")
        AddFilter(euler_filter, "X Euler", "X", "X Euler")
        AddFilter(euler_filter, "Y Euler", "Y", "Y Euler")
        AddFilter(euler_filter, "Z Euler", "Z", "Z Euler")

        scale_filter = filter_group_transform.row()
        AddFilter(scale_filter, "Scale", "Scale", "Scale")
        AddFilter(scale_filter, "X Scale", "X", "X Scale")
        AddFilter(scale_filter, "Y Scale", "Y", "Y Scale")
        AddFilter(scale_filter, "Z Scale", "Z", "Z Scale")

        filter_group_quat = layout.box()

        quat_filter = filter_group_quat.row()
        AddFilter(quat_filter, "Quaternion", "Quat", "Quaternion")
        AddFilter(quat_filter, "W Quaternion", "W", "W Quaternion")
        AddFilter(quat_filter, "X Quaternion", "X", "X Quaternion")
        AddFilter(quat_filter, "Y Quaternion", "Y", "Y Quaternion")
        AddFilter(quat_filter, "Z Quaternion", "Z", "Z Quaternion")

        filter_group_all = layout.box()

        all_filter = filter_group_all.row()
        AddFilter(all_filter, "", "ALL", "ALL")
        AddFilter(all_filter, "XOXOXOXOXOXOXO", "NONE", "NONE")


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
