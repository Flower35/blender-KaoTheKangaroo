################################################################
# "KAO2/eAmbientLight.py"

from .eLight import (KAO2_eLight, KAO2_E_LIGHT_TYPEINFO)

class KAO2_eAmbientLight(KAO2_eLight):

    def __init__(self) -> None:

        KAO2_eLight.__init__(self)

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_AMBIENTLIGHT_TYPEINFO


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_AMBIENTLIGHT_TYPEINFO = KAO2_TypeInfo (
    0x03454503,
    "eAmbientLight",
    KAO2_E_LIGHT_TYPEINFO,
    lambda: KAO2_eAmbientLight()
)


################################################################
