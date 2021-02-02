################################################################
# "KAO2/eSoundCtrl.py"

from .Basic import KAO2_Serializable

class KAO2_eSoundKey(KAO2_Serializable):

    def __init__(self) -> None:

        self.time = 0
        self.sampleName = KAO2_eString()
        self.volume = 1.0
        self.unknown_0C = False

    def serialize(self, ar: "KAO2_Archive") -> None:

        self._serializeFloat(ar, "time")
        self._serializeString(ar, "sampleName")
        self._serializeFloat(ar, "volume")
        self._serializeUInt8(ar, "unknown_0C")


from .eRefCounter import (KAO2_eRefCounter, KAO2_E_REFCOUNTER_TYPEINFO)

class KAO2_eSoundCtrl(KAO2_eRefCounter):

    def __init__(self):

        self.unknown_08 = [0, 0, 0, 0]
        self.keys = []

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_SOUNDCTRL_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        assert 4 == len(self.unknown_08)
        self._serializeFloatArray(ar, "unknown_08", False)

        self._serializeSerializables(ar, "keys", KAO2_eSoundKey, None, True)


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_SOUNDCTRL_TYPEINFO = KAO2_TypeInfo (
    0x44444555,
    "eSoundCtrl",
    KAO2_E_REFCOUNTER_TYPEINFO,
    lambda: KAO2_eSoundCtrl()
)

from .eString import KAO2_eString


################################################################
