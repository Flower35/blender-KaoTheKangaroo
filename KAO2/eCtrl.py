################################################################
# "KAO2/eCtrl.py"

import bpy
from typing import List

from .eRefCounter import (KAO2_eRefCounter, KAO2_E_REFCOUNTER_TYPEINFO)

from .Basic import (KAO2_eSRP, KAO2_ePoint3, KAO2_eQuat, KAO2_ePoint1)

class KAO2_eCtrl(KAO2_eRefCounter):

    def __init__(self, subclass_type: type) -> None:

        if subclass_type not in (KAO2_eSRP, KAO2_ePoint3, KAO2_eQuat, KAO2_ePoint1):
            raise Exception("[KAO2] eCtrl::__init__():\n\t" + "Invalid subclass type!")

        self._subclass_type = subclass_type

    def getType(self: "KAO2_eCtrl") -> "KAO2_TypeInfo":

        if KAO2_eSRP is self._subclass_type:
            return KAO2_E_CTRL_SRP_TYPEINFO

        elif KAO2_ePoint3 is self._subclass_type:
            return KAO2_E_CTRL_POINT3_TYPEINFO

        elif KAO2_eQuat is self._subclass_type:
            return KAO2_E_CTRL_QUAT_TYPEINFO

        elif KAO2_ePoint1 is self._subclass_type:
            return KAO2_E_CTRL_FLOAT_TYPEINFO

        return None

    def ctrlGenerateBlenderFCurves(self, anim_id: int, bone_name: str) -> None:

        raise Exception("[KAO2] eCtrl::ctrlGenerateBlenderFCurves():\n\t" + "OUT OF CONTEXT!")

    def ctrlCollectKeyframes(self, index: int, curves: List[bpy.types.FCurve]) -> None:

        raise Exception("[KAO2] eCtrl::ctrlCollectKeyframes():\n\t" + "OUT OF CONTEXT!")


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_CTRL_SRP_TYPEINFO = KAO2_TypeInfo (
    0x9002,
    "eCtrl<eSRP>",
    KAO2_E_REFCOUNTER_TYPEINFO,
    lambda: None
)

KAO2_E_CTRL_POINT3_TYPEINFO = KAO2_TypeInfo (
    0x9003,
    "eCtrl<ePoint3>",
    KAO2_E_REFCOUNTER_TYPEINFO,
    lambda: None
)

KAO2_E_CTRL_QUAT_TYPEINFO = KAO2_TypeInfo (
    0x9005,
    "eCtrl<eQuat>",
    KAO2_E_REFCOUNTER_TYPEINFO,
    lambda: None
)

KAO2_E_CTRL_FLOAT_TYPEINFO = KAO2_TypeInfo (
    0x9006,
    "eCtrl<float>",
    KAO2_E_REFCOUNTER_TYPEINFO,
    lambda: None
)


################################################################
