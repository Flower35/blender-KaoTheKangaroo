################################################################
# "KAO2/eProxy.py"

from .eTransform import (KAO2_eTransform, KAO2_E_TRANSFORM_TYPEINFO)

class KAO2_eProxy(KAO2_eTransform):

    def __init__(self) -> None:

        KAO2_eTransform.__init__(self)

        self.targetFile = KAO2_eString()
        self.category = 0

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_PROXY_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        KAO2_eTransform.serialize(self, ar)

        self._serializeString(ar, "targetFile")
        self._serializeUInt32(ar, "category")


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_PROXY_TYPEINFO = KAO2_TypeInfo (
    0x13454032,
    "eProxy",
    KAO2_E_TRANSFORM_TYPEINFO,
    lambda: KAO2_eProxy()
)

from .eString import KAO2_eString


################################################################
