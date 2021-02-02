################################################################
# "KAO2/eFogEnv.py"

from .eRefCounter import (KAO2_eRefCounter, KAO2_E_REFCOUNTER_TYPEINFO)

class KAO2_eFogEnv(KAO2_eRefCounter):

    def __init__(self) -> None:

        self.fogColor = [1.0, 0, 1.0]
        self.fogStart = (-1.0)
        self.fogEnd = 1.0
        self.fogMax = (-1.0)

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_FOGENV_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        assert 3 == len(self.fogColor)
        self._serializeFloatArray(ar, "fogColor", False)

        self._serializeFloat(ar, "fogStart")
        self._serializeFloat(ar, "fogEnd")
        self._serializeFloat(ar, "fogMax")


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_FOGENV_TYPEINFO = KAO2_TypeInfo (
    0x3F800002,
    "eFogEnv",
    KAO2_E_REFCOUNTER_TYPEINFO,
    lambda: KAO2_eFogEnv()
)


################################################################
