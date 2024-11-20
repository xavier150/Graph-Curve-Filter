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

'''
This addons allows to easily add filter in graph editor.

Addon for Blender by Xavier Loux (BleuRaven)
xavierloux.com
xavierloux.loux@gmail.com
'''

import os
import bpy
import fnmatch
import time
import addon_utils

from . import gcf_addon_pref
from . import gcf_ui
from . import gcf_basics
from . import gcf_utils

if "bpy" in locals():
    import importlib
    if "gcf_addon_pref" in locals():
        importlib.reload(gcf_addon_pref)
    if "gcf_ui" in locals():
        importlib.reload(gcf_ui)
    if "gcf_export_asset" in locals():
        importlib.reload(gcf_export_asset)
    if "gcf_write_text" in locals():
        importlib.reload(gcf_write_text)
    if "gcf_basics" in locals():
        importlib.reload(gcf_basics)
    if "gcf_utils" in locals():
        importlib.reload(gcf_utils)

bl_info = {}

classes = (
)


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    gcf_addon_pref.register()
    gcf_ui.register()


def unregister():
    from bpy.utils import unregister_class

    for cls in classes:
        unregister_class(cls)

    gcf_addon_pref.unregister()
    gcf_ui.unregister()
