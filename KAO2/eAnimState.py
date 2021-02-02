################################################################
# "KAO2/eAnimState.py"

from .eRefCounter import (KAO2_eRefCounter, KAO2_E_REFCOUNTER_TYPEINFO)

class KAO2_eAnimState(KAO2_eRefCounter):

    def __init__(self) -> None:

        self.aID = 0
        self.unknown_0C = 1.0
        self.time = 0
        self.unknown_14 = 0
        self.citt = 0
        self.pitt = 0
        self.cott = 0
        self.pott = 0
        self.bt = 0
        self.bs = 0
        self.w = 1.0
        self.startFrame = 0
        self.endFrame = 0
        self.loopType = 1
        self.bef = 0
        self.bet = 0

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_ANIMSTATE_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        self._serializeUInt32(ar, "aID")
        self._serializeFloat(ar, "unknown_0C")
        self._serializeFloat(ar, "time")
        self._serializeFloat(ar, "citt")
        self._serializeFloat(ar, "pitt")
        self._serializeFloat(ar, "bt")
        self._serializeFloat(ar, "bs")
        self._serializeFloat(ar, "w")
        self._serializeUInt32(ar, "loopType")
        self._serializeFloat(ar, "startFrame")
        self._serializeFloat(ar, "endFrame")
        self._serializeFloat(ar, "unknown_14")
        self._serializeFloat(ar, "cott")
        self._serializeFloat(ar, "pott")
        self._serializeFloat(ar, "bef")
        self._serializeFloat(ar, "bet")


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_ANIMSTATE_TYPEINFO = KAO2_TypeInfo (
    0xAC000001,
    "eAnimState",
    KAO2_E_REFCOUNTER_TYPEINFO,
    lambda: KAO2_eAnimState()
)


################################################################
