################################################################
# "KAO2/eBillboard.py"

from .eTransform import (KAO2_eTransform, KAO2_E_TRANSFORM_TYPEINFO)

class KAO2_eBillboard(KAO2_eTransform):

    def __init__(self) -> None:

        KAO2_eTransform.__init__(self)

        self.billboarded = True

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_BILLBOARD_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        KAO2_eTransform.serialize(self, ar)

        self._serializeUInt8(ar, "billboarded")


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_BILLBOARD_TYPEINFO = KAO2_TypeInfo (
    0x00008222,
    "eBillboard",
    KAO2_E_TRANSFORM_TYPEINFO,
    lambda: KAO2_eBillboard()
)


################################################################
