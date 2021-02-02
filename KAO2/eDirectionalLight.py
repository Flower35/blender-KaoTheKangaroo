################################################################
# "KAO2/eDirectionalLight.py"

from .Basic import KAO2_ePoint3

from .eLight import (KAO2_eLight, KAO2_E_LIGHT_TYPEINFO)

class KAO2_eDirectionalLight(KAO2_eLight):

    def __init__(self) -> None:

        KAO2_eLight.__init__(self)

        self.position = KAO2_ePoint3()
        self.target = None

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_DIRECTIONALLIGHT_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        KAO2_eLight.serialize(self, ar)

        self.position.serialize(ar)

        from .eTransform import KAO2_E_TRANSFORM_TYPEINFO
        self._serializeRefObject(ar, "target", KAO2_E_TRANSFORM_TYPEINFO)


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_DIRECTIONALLIGHT_TYPEINFO = KAO2_TypeInfo (
    0x03454501,
    "eDirectionalLight",
    KAO2_E_LIGHT_TYPEINFO,
    lambda: KAO2_eDirectionalLight()
)


################################################################
