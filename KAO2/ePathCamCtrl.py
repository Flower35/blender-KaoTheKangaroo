################################################################
# "KAO2/ePathCamCtrl.py"

from .eRefCounter import (KAO2_eRefCounter, KAO2_E_REFCOUNTER_TYPEINFO)

class KAO2_ePathCamCtrl(KAO2_eRefCounter):

    def __init__(self) -> None:

        self.camera = None
        self.bezier = None
        self.position = KAO2_ePoint3()
        self.unknown_1C = 0
        self.unknown_20_A = 0x00
        self.unknown_20_B = 0x01
        self.unknown_20_C = 0x00
        self.unknown_20_D = 0x01
        self.unknown_24 = 0
        self.unknown_28 = 180.0
        self.unknown_38 = 0

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_PATHCAMCTRL_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        self._serializeRefObject(ar, "camera", KAO2_E_CAMERA_TYPEINFO)

        test = [1]
        ar.file.parseUInt32(test)
        if 1 != test[0]:
            raise Exception("[KAO2] ePathCamCtrl::serialize():\n\t" + "non-empty member is not supported!")

        self._serializeFloat(ar, "unknown_38")
        self._serializeFloat(ar, "unknown_24")

        self._serializeRefObject(ar, "bezier", KAO2_E_BEZIERSPLINENODE_TYPEINFO)

        self._serializeFloat(ar, "unknown_1C")
        self._serializeUInt8(ar, "unknown_20_A")
        self._serializeUInt8(ar, "unknown_20_B")

        self.position.serialize(ar)

        self._serializeFloat(ar, "unknown_28")
        self._serializeUInt8(ar, "unknown_20_C")
        self._serializeUInt8(ar, "unknown_20_D")


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_PATHCAMCTRL_TYPEINFO = KAO2_TypeInfo (
    0x12455671,
    "ePathCamCtrl",
    KAO2_E_REFCOUNTER_TYPEINFO,
    lambda: KAO2_ePathCamCtrl()
)

from .Basic import KAO2_ePoint3
from .eCamera import KAO2_E_CAMERA_TYPEINFO
from .eBezierSplineNode import KAO2_E_BEZIERSPLINENODE_TYPEINFO


################################################################
