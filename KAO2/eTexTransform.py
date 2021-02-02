################################################################
# "KAO2/eTexTransform.py"

from .eRefCounter import (KAO2_eRefCounter, KAO2_E_REFCOUNTER_TYPEINFO)

class KAO2_eTexTransform(KAO2_eRefCounter):

    def __init__(self) -> None:

        self.xScale = None
        self.yScale = None
        self.uOffset = None
        self.vOffset = None

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_TEXTRANSFORM_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        self._serializeRefObject(ar, "xScale", KAO2_E_LEAFCTRL_FLOAT_TYPEINFO)
        self._serializeRefObject(ar, "yScale", KAO2_E_LEAFCTRL_FLOAT_TYPEINFO)
        self._serializeRefObject(ar, "uOffset", KAO2_E_LEAFCTRL_FLOAT_TYPEINFO)
        self._serializeRefObject(ar, "vOffset", KAO2_E_LEAFCTRL_FLOAT_TYPEINFO)


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo
from .eLeafCtrl import KAO2_E_LEAFCTRL_FLOAT_TYPEINFO

KAO2_E_TEXTRANSFORM_TYPEINFO = KAO2_TypeInfo (
    0x1004,
    "eTexTransform",
    KAO2_E_REFCOUNTER_TYPEINFO,
    lambda: KAO2_eTexTransform()
)


################################################################
