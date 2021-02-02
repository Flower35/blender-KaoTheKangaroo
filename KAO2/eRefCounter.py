################################################################
# "KAO2/eRefCounter.py"

from .eObject import (KAO2_eObject, KAO2_E_OBJECT_TYPEINFO)

class KAO2_eRefCounter(KAO2_eObject):

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_REFCOUNTER_TYPEINFO


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_REFCOUNTER_TYPEINFO = KAO2_TypeInfo (
    0x200D,
    "eRefCounter",
    KAO2_E_OBJECT_TYPEINFO,
    lambda: KAO2_eRefCounter()
)


################################################################
