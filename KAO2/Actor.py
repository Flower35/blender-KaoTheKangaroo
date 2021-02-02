################################################################
# "KAO2/Actor.py"

from .ePivot import (KAO2_ePivot, KAO2_E_PIVOT_TYPEINFO)

class KAO2_Actor(KAO2_ePivot):

    def __init__(self) -> None:

        KAO2_ePivot.__init__(self)

        self.script = None
        self.scriptPath = KAO2_eString()
        self.unknown_04D0 = []
        self.unknown_04DC = []

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_ACTOR_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        KAO2_ePivot.serialize(self, ar)

        test = [1]
        ar.file.parseUInt32(test)
        if 1 != test[0]:
            raise Exception("[KAO2] Actor::serialize():\n\t" + "non-empty \"Namespace\" is not supported!")

        self._serializeString(ar, "scriptPath")

        if ar.version >= 0x89:

            for i in range (0, 2):
                test = [0]
                ar.file.parseUInt32(test)
                if 0 != test[0]:
                    raise Exception("[KAO2] Actor::serialize():\n\t" + "\"gadgets\" and \"noderefs\" are not supported!")


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_ACTOR_TYPEINFO = KAO2_TypeInfo (
    0x07EA0000,
    "Actor",
    KAO2_E_PIVOT_TYPEINFO,
    lambda: KAO2_Actor()
)

from .eString import KAO2_eString


################################################################
