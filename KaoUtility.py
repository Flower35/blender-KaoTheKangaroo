################################################################
# "KaoUtility.py"

import bpy
from typing import Tuple

class KaoSettings():

    def __init__(self) -> None:

        self.reset()

    def reset(self) -> None:

        self.workspaceDir = ""
        self.blenderObjData = None
        self.blenderObjTransform = [(0, 0, 0), (1, 0, 0, 0), (1, 1, 1)]
        self.armatureParent = None
        self.armatureBoneXforms = []
        self.armatureModifiedMeshes = []
        self.worldMatrix = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        self.actionsList = []
        self.ignoreInvBindMatrices = False
        self.ignoreRestPoseUseShapeKeys = False


Settings = KaoSettings()


################################################################

def link_objects_to_scene_collection(obj: bpy.types.Object) -> None:

    if obj.name not in bpy.context.collection.objects:
        bpy.context.collection.objects.link(obj)

    for child in obj.children:
        link_objects_to_scene_collection(child)


def push_active_obj() -> Tuple[bpy.types.Object, str]:

    obj = bpy.context.view_layer.objects.active
    mode = bpy.context.object.mode if (bpy.context.object is not None) else "OBJECT"

    return obj, mode


def pop_active_obj(obj: bpy.types.Object, mode: str) -> None:

    bpy.context.view_layer.objects.active = obj

    if obj is not None:
        bpy.ops.object.mode_set(mode = mode)


################################################################
