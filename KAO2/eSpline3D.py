################################################################
# "KAO2/eSpline3D.py"

from .Basic import KAO2_Serializable

class KAO2_eSplineVertex(KAO2_Serializable):

    def __init__(self) -> None:

        self.centerPos = KAO2_ePoint3()
        self.leftPos = KAO2_ePoint3()
        self.rightPos = KAO2_ePoint3()
        self.name = KAO2_eString()

    def serialize(self, ar: "KAO2_Archive") -> None:

        self.centerPos.serialize(ar)
        self.leftPos.serialize(ar)
        self.rightPos.serialize(ar)

        self._serializeString(ar, "name")


from .eRefCounter import (KAO2_eRefCounter, KAO2_E_REFCOUNTER_TYPEINFO)

class KAO2_eSpline3D(KAO2_eRefCounter):

    def __init__(self):

        self.vertices = []
        self.unknown_14 = 0

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_SPLINE3D_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        self._serializeSerializables(ar, "vertices", KAO2_eSplineVertex, None, True)

        self._serializeFloat(ar, "unknown_14")

    def addVertex(self, new_center: "KAO2_ePoint3", new_left: "KAO2_ePoint3", new_right: "KAO2_ePoint3", new_name: "KAO2_eString") -> None:

        if (len(self.vertices) > 0) and (self.vertices[-1].centerPos == new_center):

            vertices[-1].leftPos = (vertices[-1].leftPos + new_left) * 0.5
            vertices[-1].rightPos = (vertices[-1].rightPos + new_right) * 0.5

            if len(new_name.text) > 0:
                vertices[-1].name = new_name

        else:

            vertices.append(KAO2_eSplineVertexBase())

            vertices[-1].centerPos = new_center
            vertices[-1].leftPos = new_left
            vertices[-1].rightPos = new_right
            vertices[-1].name = new_name

    def appendVerticesFromSpline(self, other: "KAO2_eSpline3D") -> None:

        for i in range(0, len(other.vertices)):

            self.addVertex (
                other.vertices[i].centerPos,
                other.vertices[i].leftPos,
                other.vertices[i].rightPos,
                other.vertices[i].name )


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_SPLINE3D_TYPEINFO = KAO2_TypeInfo (
    0x64716E01,
    "eSpline3D",
    KAO2_E_REFCOUNTER_TYPEINFO,
    lambda: KAO2_eSpline3D()
)

from .Basic import KAO2_ePoint3
from .eString import KAO2_eString


################################################################
