# SPDX-FileCopyrightText: 2021-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Graph Curve Filter
#  https://github.com/xavier150/Graph-Curve-Filter
# ----------------------------------------------

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

from . import bpl
from . import bbpl
from . import gcf_addon_pref
from . import gcf_ui
from . import gcf_basics
from . import gcf_utils

if "bpy" in locals():
    import importlib
    if "bpl" in locals():
        importlib.reload(bpl)
    if "bbpl" in locals():
        importlib.reload(bbpl)
    if "gcf_addon_pref" in locals():
        importlib.reload(gcf_addon_pref)
    if "gcf_ui" in locals():
        importlib.reload(gcf_ui)
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

    bbpl.register()
    gcf_addon_pref.register()
    gcf_ui.register()


def unregister():
    from bpy.utils import unregister_class

    for cls in classes:
        unregister_class(cls)

    gcf_addon_pref.unregister()
    gcf_ui.unregister()
    bbpl.unregister()