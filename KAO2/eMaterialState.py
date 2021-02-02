################################################################
# "KAO2/eMaterialState.py"

from .eRefCounter import (KAO2_eRefCounter, KAO2_E_REFCOUNTER_TYPEINFO)

class KAO2_eMaterialState(KAO2_eRefCounter):

    def __init__(self) -> None:

        self.ambient = [0.5, 0.5, 0.5, 1.0]
        self.diffuse = [0.5, 0.5, 0.5, 1.0]
        self.emissive = [0, 0, 0, 1.0]
        self.specular = [0.5, 0.5, 0.5, 1.0]
        self.shininess = 0
        self.useGlobalAmbientLight = True

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_MATERIALSTATE_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        assert 4 == len(self.diffuse)
        self._serializeFloatArray(ar, "diffuse", False)

        assert 4 == len(self.ambient)
        self._serializeFloatArray(ar, "ambient", False)

        assert 4 == len(self.emissive)
        self._serializeFloatArray(ar, "emissive", False)

        assert 4 == len(self.specular)
        self._serializeFloatArray(ar, "specular", False)

        self._serializeFloat(ar, "shininess")

        self._serializeUInt8(ar, "useGlobalAmbientLight")


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_MATERIALSTATE_TYPEINFO = KAO2_TypeInfo (
    0x1005,
    "eMaterialState",
    KAO2_E_REFCOUNTER_TYPEINFO,
    lambda: KAO2_eMaterialState()
)


################################################################
