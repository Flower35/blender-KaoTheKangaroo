################################################################
# "KAO2/eLight.py"

from .eNode import (KAO2_eNode, KAO2_E_NODE_TYPEINFO)

class KAO2_eLight(KAO2_eNode):

    def __init__(self) -> None:

        KAO2_eNode.__init__(self)

        self.diffuseColor = [1.0, 1.0, 1.0, 1.0]
        self.ambientColor = [1.0, 1.0, 1.0, 1.0]
        self.specularColor = [0, 0, 0, 0]

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_LIGHT_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        KAO2_eNode.serialize(self, ar)

        assert 4 == len(self.diffuseColor)
        self._serializeFloatArray(ar, "diffuseColor", False)

        assert 4 == len(self.ambientColor)
        self._serializeFloatArray(ar, "ambientColor", False)

        assert 4 == len(self.specularColor)
        self._serializeFloatArray(ar, "specularColor", False)


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_LIGHT_TYPEINFO = KAO2_TypeInfo (
    0x03454500,
    "eLight",
    KAO2_E_NODE_TYPEINFO,
    lambda: None
)

from .eString import KAO2_eString


################################################################
