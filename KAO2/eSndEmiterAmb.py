################################################################
# "KAO2/eSndEmiterAmb.py"

from .eSndEmiter import (KAO2_eSndEmiter, KAO2_E_SNDEMITER_TYPEINFO)

class KAO2_eSndEmiterAmb(KAO2_eSndEmiter):

    def __init__(self) -> None:

        KAO2_eSndEmiter.__init__(self)

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_SNDEMITERAMB_TYPEINFO


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_SNDEMITERAMB_TYPEINFO = KAO2_TypeInfo (
    0x09994523,
    "eSndEmiterAmb",
    KAO2_E_SNDEMITER_TYPEINFO,
    lambda: KAO2_eSndEmiterAmb()
)


################################################################
