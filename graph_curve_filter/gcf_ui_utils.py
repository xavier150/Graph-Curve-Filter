# SPDX-FileCopyrightText: 2021-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Graph Curve Filter
#  https://github.com/xavier150/Graph-Curve-Filter
# ----------------------------------------------


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


def LayoutSection(layout, PropName, PropLabel):
    scene = bpy.context.scene
    expanded = eval("scene."+PropName)
    tria_icon = "TRIA_DOWN" if expanded else "TRIA_RIGHT"
    layout.row().prop(scene, PropName, icon=tria_icon, icon_only=True, text=PropLabel, emboss=False)
    return expanded
