################################################################
# "KAO2/eSndEmiter.py"

from .eTransform import (KAO2_eTransform, KAO2_E_TRANSFORM_TYPEINFO)

class KAO2_eSndEmiter(KAO2_eTransform):

    def __init__(self) -> None:

        KAO2_eTransform.__init__(self)

        self.controllers = []

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_SNDEMITER_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        KAO2_eTransform.serialize(self, ar)

        self._serializeRefObjectArray(ar, "controllers", KAO2_E_SOUNDCTRL_TYPEINFO)

        test = [0]
        ar.file.parseUInt32(test)
        if 0 != test[0]:
            raise Exception("[KAO2] eSndEmiter::serialize():\n\t" + "ar.version() no longer supported. THIS SHOULD NEVER HAPPEN.")


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_SNDEMITER_TYPEINFO = KAO2_TypeInfo (
    0x12345567,
    "eSndEmiter",
    KAO2_E_TRANSFORM_TYPEINFO,
    lambda: None
)

from .eSoundCtrl import KAO2_E_SOUNDCTRL_TYPEINFO


################################################################
