################################################################
# "KAO2/eSndEmiterOmni.py"

from .eSndEmiter import (KAO2_eSndEmiter, KAO2_E_SNDEMITER_TYPEINFO)

class KAO2_eSndEmiterOmni(KAO2_eSndEmiter):

    def __init__(self) -> None:

        KAO2_eSndEmiter.__init__(self)

        self.unknown_C8 = 1.0
        self.unknown_CC = 1.0

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_SNDEMITEROMNI_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        KAO2_eSndEmiter.serialize(self, ar)

        self._serializeFloat(ar, "unknown_C8")
        self._serializeFloat(ar, "unknown_CC")


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_SNDEMITEROMNI_TYPEINFO = KAO2_TypeInfo (
    0x09994525,
    "eSndEmiterOmni",
    KAO2_E_SNDEMITER_TYPEINFO,
    lambda: KAO2_eSndEmiterOmni()
)


################################################################
