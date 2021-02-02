################################################################
# "KAO2/eTrack.py"

from .eRefCounter import (KAO2_eRefCounter, KAO2_E_REFCOUNTER_TYPEINFO)

class KAO2_eTrack(KAO2_eRefCounter):

    def __init__(self) -> None:

        self.name = KAO2_eString()
        self.startFrame = 0
        self.endFrame = 0
        self.loopType = 0

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_TRACK_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        self._serializeString(ar, "name")
        self._serializeFloat(ar, "startFrame")
        self._serializeFloat(ar, "endFrame")
        self._serializeUInt32(ar, "loopType")


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_TRACK_TYPEINFO = KAO2_TypeInfo (
    0xAC000000,
    "eTrack",
    KAO2_E_REFCOUNTER_TYPEINFO,
    lambda: KAO2_eTrack()
)

from .eString import KAO2_eString


################################################################
