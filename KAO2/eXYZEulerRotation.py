################################################################
# "KAO2/eXYZEulerRotation.py"

import bpy
from typing import List

from .Basic import KAO2_eQuat
from .eCtrl import (KAO2_eCtrl, KAO2_E_CTRL_QUAT_TYPEINFO)

class KAO2_eXYZEulerRotation(KAO2_eCtrl):

    def __init__(self) -> None:

        KAO2_eCtrl.__init__(self, KAO2_eQuat)

        self.xCtrl = None
        self.yCtrl = None
        self.zCtrl = None
        self.unknown_14 = 0x24

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_XYZEULERROTATION_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        self._serializeRefObject(ar, "xCtrl", KAO2_E_LEAFCTRL_FLOAT_TYPEINFO)
        self._serializeRefObject(ar, "yCtrl", KAO2_E_LEAFCTRL_FLOAT_TYPEINFO)
        self._serializeRefObject(ar, "zCtrl", KAO2_E_LEAFCTRL_FLOAT_TYPEINFO)

        self._serializeUInt32(ar, "unknown_14")

    def ctrlGenerateBlenderFCurves(self, anim_id: int, bone_name: str) -> None:

        raise Exception("[KAO2] eXYZEulerRotation::ctrlGenerateBlenderFCurves():\n\t" + "OUT OF CONTEXT!")

    def ctrlCollectKeyframes(self, index: int, curves: List[bpy.types.FCurve]) -> None:

        if self.xCtrl is not None:
            self.xCtrl.ctrlCollectKeyframes(0, curves)
        else:
            curves[0].keyframe_points.add(1)
            curves[0].keyframe_points[0].co = [0, 0]
            curves[0].keyframe_points[0].interpolation = "CONSTANT"

        if self.yCtrl is not None:
            self.yCtrl.ctrlCollectKeyframes(1, curves)
        else:
            curves[1].keyframe_points.add(1)
            curves[1].keyframe_points[0].co = [0, 0]
            curves[1].keyframe_points[0].interpolation = "CONSTANT"

        if self.zCtrl is not None:
            self.zCtrl.ctrlCollectKeyframes(2, curves)
        else:
            curves[2].keyframe_points.add(1)
            curves[2].keyframe_points[0].co = [0, 0]
            curves[2].keyframe_points[0].interpolation = "CONSTANT"


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_XYZEULERROTATION_TYPEINFO = KAO2_TypeInfo (
    0x9040,
    "eXYZEulerRotation",
    KAO2_E_CTRL_QUAT_TYPEINFO,
    lambda: KAO2_eXYZEulerRotation()
)

from .eLeafCtrl import KAO2_E_LEAFCTRL_FLOAT_TYPEINFO


################################################################
