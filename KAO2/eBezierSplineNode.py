################################################################
# "KAO2/eBezierSplineNode.py"

from .eNode import (KAO2_eNode, KAO2_E_NODE_TYPEINFO)

class KAO2_eBezierSplineNode(KAO2_eNode):

    def __init__(self) -> None:

        KAO2_eNode.__init__(self)

        self.spline = None

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_BEZIERSPLINENODE_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        KAO2_eNode.serialize(self, ar)

        dummy_spline = [None]

        test = [0 if self.spline is None else 1]
        ar.file.parseUInt32(test)

        for i in range(0, test[0]):

            if 0 == i:

                self._serializeRefObject(ar, "spline", KAO2_E_SPLINE3D_TYPEINFO)

            else:

                ar.serialize(dummy_spline, 0, KAO2_E_SPLINE3D_TYPEINFO)

                if (self.spline is not None) and (dummy_spline[0] is not None):

                    self.spline.appendVerticesFromSpline(dummy_spline[0])


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_BEZIERSPLINENODE_TYPEINFO = KAO2_TypeInfo (
    0x00398884,
    "eBezierSplineNode",
    KAO2_E_NODE_TYPEINFO,
    lambda: KAO2_eBezierSplineNode()
)

from .eSpline3D import KAO2_E_SPLINE3D_TYPEINFO


################################################################
