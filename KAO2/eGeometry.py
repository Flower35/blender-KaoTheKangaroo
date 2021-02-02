################################################################
# "KAO2/eGeometry.py"

import bpy

from .Basic import KAO2_ePoint3
from .eNode import (KAO2_eNode, KAO2_E_NODE_TYPEINFO)

class KAO2_eGeometry(KAO2_eNode):

    def __init__(self) -> None:

        KAO2_eNode.__init__(self)

        self.material = None
        self.boxBoundMin = KAO2_ePoint3()
        self.boxBoundMax = KAO2_ePoint3()

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_GEOMETRY_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        KAO2_eNode.serialize(self, ar)

        self._serializeRefObject(ar, "material", KAO2_E_MATERIAL_TYPEINFO)

        self.boxBoundMin.serialize(ar)
        self.boxBoundMax.serialize(ar)

    def toBlenderObject(self) -> bpy.types.Object:

        if self.blenderObj is not None:
            return self.blenderObj

        obj = KAO2_eNode.toBlenderObject(self)

        if self.material is not None:
            self.material.toBlenderObject()

        self.blenderObj = obj
        return obj


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_GEOMETRY_TYPEINFO = KAO2_TypeInfo (
    0x034567FD,
    "eGeometry",
    KAO2_E_NODE_TYPEINFO,
    lambda: None
)

from .eMaterial import KAO2_E_MATERIAL_TYPEINFO


################################################################
