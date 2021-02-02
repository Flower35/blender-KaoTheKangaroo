################################################################
# "KAO2/eSRPCombineCtrl.py"

import bpy
from typing import List

from ..KaoUtility import *

from .Basic import KAO2_eSRP
from .eCtrl import (KAO2_eCtrl, KAO2_E_CTRL_SRP_TYPEINFO, KAO2_E_CTRL_QUAT_TYPEINFO, KAO2_E_CTRL_POINT3_TYPEINFO)

class KAO2_eSRPCombineCtrl(KAO2_eCtrl):

    def __init__(self) -> None:

        KAO2_eCtrl.__init__(self, KAO2_eSRP)

        self.sclCtrl = None
        self.rotCtrl = None
        self.posCtrl = None

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_SRPCOMBINECTRL_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        self._serializeRefObject(ar, "sclCtrl", KAO2_E_LEAFCTRL_FLOAT_TYPEINFO)
        self._serializeRefObject(ar, "rotCtrl", KAO2_E_CTRL_QUAT_TYPEINFO)
        self._serializeRefObject(ar, "posCtrl", KAO2_E_CTRL_POINT3_TYPEINFO)

    def ctrlGenerateBlenderFCurves(self, anim_id: int, bone_name: str) -> None:

        _debug_header = "[KAO2] eSRPCombineCtrl::ctrlGenerateBlenderFCurves():\n\t"

        if (anim_id < 0) or (anim_id >= len(Settings.actionsList)):
            raise Exception(_debug_header + "Too many animations!")

        action = Settings.actionsList[anim_id]

        scl_curves = []
        rot_curves = []
        pos_curves = []

        rna_path = "pose.bones[\"{}\"].".format(bone_name) if bone_name else ""
        group = action.groups.new(name = bone_name if bone_name else "Object Transforms")

        ################################

        for i in range (0, 3):
            curve = action.fcurves.new(data_path = rna_path + "scale", index = i)
            curve.group = group
            scl_curves.append(curve)

        if self.sclCtrl is not None:
            if self.sclCtrl.getType() is KAO2_E_LEAFCTRL_FLOAT_TYPEINFO:
                for i in range (0, 3):
                    self.sclCtrl.ctrlCollectKeyframes(i, scl_curves)
            else:
                raise Exception(_debug_header + "Invalid controller type for scale keyframes!")
        else:
            for i in range (0, 3):
                scl_curves[i].keyframe_points.add(1)
                scl_curves[i].keyframe_points[0].co = [0, 1.0]
                scl_curves[i].keyframe_points[0].interpolation = "CONSTANT"

        ################################

        if self.rotCtrl is not None:
            if self.rotCtrl.getType() is KAO2_E_LEAFCTRL_QUAT_TYPEINFO:
                for i in range (0, 4):
                    curve = action.fcurves.new(data_path = rna_path + "rotation_quaternion", index = i)
                    curve.group = group
                    rot_curves.append(curve)
                self.rotCtrl.ctrlCollectKeyframes((-1), rot_curves)
            elif self.rotCtrl.getType() is KAO2_E_XYZEULERROTATION_TYPEINFO:
                for i in range (0, 3):
                    curve = action.fcurves.new(data_path = rna_path + "rotation_euler", index = i)
                    curve.group = group
                    rot_curves.append(curve)
                self.rotCtrl.ctrlCollectKeyframes((-1), rot_curves)
            else:
                raise Exception(_debug_header + "Invalid controller type for rotation keyframes!")
        else:
            for i in range (0, 4):
                curve = action.fcurves.new(data_path = rna_path + "rotation_quaternion", index = i)
                curve.group = group
                curve.keyframe_points.add(1)
                curve.keyframe_points[0].co = [0, 1.0 if (0 == i) else 0]
                curve.keyframe_points[0].interpolation = "CONSTANT"

        ################################

        for i in range (0, 3):
            curve = action.fcurves.new(data_path = rna_path + "location", index = i)
            curve.group = group
            pos_curves.append(curve)

        if self.posCtrl is not None:
            if self.posCtrl.getType() in (KAO2_E_LEAFCTRL_POINT3_TYPEINFO, KAO2_E_XYZPOINT3CTRL_TYPEINFO):
                self.posCtrl.ctrlCollectKeyframes((-1), pos_curves)
            else:
                raise Exception(_debug_header + "Invalid controller type for position keyframes!")
        else:
            for i in range (0, 3):
                pos_curves[i].keyframe_points.add(1)
                pos_curves[i].keyframe_points[0].co = [0, 0]
                pos_curves[i].keyframe_points[0].interpolation = "CONSTANT"

        ################################

        for curve in action.fcurves:
            curve.update()

    def ctrlCollectKeyframes(self, index: int, curves: List[bpy.types.FCurve]) -> None:

        raise Exception("[KAO2] eSRPCombineCtrl::ctrlCollectKeyframes():\n\t" + "OUT OF CONTEXT!")


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_SRPCOMBINECTRL_TYPEINFO = KAO2_TypeInfo (
    0x9020,
    "eSRPCombineCtrl",
    KAO2_E_CTRL_SRP_TYPEINFO,
    lambda: KAO2_eSRPCombineCtrl()
)

from .eLeafCtrl import (KAO2_E_LEAFCTRL_FLOAT_TYPEINFO, KAO2_E_LEAFCTRL_POINT3_TYPEINFO, KAO2_E_LEAFCTRL_QUAT_TYPEINFO)
from .eXYZEulerRotation import KAO2_E_XYZEULERROTATION_TYPEINFO
from .eXYZPoint3Ctrl import KAO2_E_XYZPOINT3CTRL_TYPEINFO


################################################################
