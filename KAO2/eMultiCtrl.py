################################################################
# "KAO2/eMultiCtrl.py"

import bpy
from typing import List

from .Basic import (KAO2_eSRP, KAO2_ePoint1)
from .eCtrl import (KAO2_eCtrl, KAO2_E_CTRL_SRP_TYPEINFO, KAO2_E_CTRL_FLOAT_TYPEINFO)

class KAO2_eMultiCtrl(KAO2_eCtrl):

    def __init__(self, subclass_type: type) -> None:

        KAO2_eCtrl.__init__(self, subclass_type)

        self.controllers = []

    def getType(self) -> "KAO2_TypeInfo":

        if KAO2_eSRP is self._subclass_type:
            return KAO2_E_MULTICTRL_SRP_TYPEINFO

        elif KAO2_ePoint1 is self._subclass_type:
            return KAO2_E_MULTICTRL_FLOAT_TYPEINFO

        return None

    def serialize(self, ar: "KAO2_Archive") -> None:

        if KAO2_eSRP is self._subclass_type:
            info = KAO2_E_SRPCOMBINECTRL_TYPEINFO

        elif KAO2_ePoint1 is self._subclass_type:
            info = KAO2_E_LEAFCTRL_FLOAT_TYPEINFO

        else:
            raise Exception("[KAO2] eMultiCtrl::serialize():\n\t" + "Invalid subclass type!")

        self._serializeRefObjectArray(ar, "controllers", info)

    def ctrlGenerateBlenderFCurves(self, anim_id: int, bone_name: str) -> None:

        for i in range (0, len(self.controllers)):
            self.controllers[i].ctrlGenerateBlenderFCurves(i, bone_name)

    def ctrlCollectKeyframes(self, index: int, curves: List[bpy.types.FCurve]) -> None:

        raise Exception("[KAO2] eMultiCtrl::ctrlCollectKeyframes():\n\t" + "OUT OF CONTEXT!")


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo
from .eSRPCombineCtrl import KAO2_E_SRPCOMBINECTRL_TYPEINFO
from .eLeafCtrl import KAO2_E_LEAFCTRL_FLOAT_TYPEINFO

KAO2_E_MULTICTRL_SRP_TYPEINFO = KAO2_TypeInfo (
    0x9010,
    "eMultiCtrl<eSRPCtrl>",
    KAO2_E_CTRL_SRP_TYPEINFO,
    lambda: KAO2_eMultiCtrl(KAO2_eSRP)
)

KAO2_E_MULTICTRL_FLOAT_TYPEINFO = KAO2_TypeInfo (
    0x9012,
    "eMultiCtrl<eFloatCtrl>",
    KAO2_E_CTRL_FLOAT_TYPEINFO,
    lambda: KAO2_eMultiCtrl(KAO2_ePoint1)
)


################################################################
