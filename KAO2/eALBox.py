################################################################
# "KAO2/eALBox.py"

import bpy

from .Basic import KAO2_Serializable

class KAO2_eAxisList(KAO2_Serializable):

    def __init__(self) -> None:

        self.previous = None
        self.next = None
        self.coordLimit = 0
        self.alboxEntryId = (-1)
        self.columnId = 0
        self.rowId = 0

    def serialize(self, ar: "KAO2_Archive") -> None:

        self._serializeFloat(ar, "coordLimit")
        self._serializeUInt16(ar, "alboxEntryId")
        self._serializeUInt8(ar, "columnId")
        self._serializeUInt8(ar, "rowId")

        self._serializeUInt32(ar, "previous")
        self._serializeUInt32(ar, "next")


from .eRefCounter import (KAO2_eRefCounter, KAO2_E_REFCOUNTER_TYPEINFO)

class KAO2_eALBox(KAO2_eRefCounter):

    def __init__(self):

        self.myScene = None
        self.parentNode = None
        self.axisList = [None] * 6
        self.series = []
        self.collisionEntryId = (-1)
        self.unknown_80 = []

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_ALBOX_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        _debug_header = "[KAO2] eALBox::serialize():\n\t"

        if not ar.isInReadMode:
            raise Exception(_debug_header + "saving not supported!")

        from .eScene import KAO2_E_SCENE_TYPEINFO
        from .eNode import KAO2_E_NODE_TYPEINFO

        self._serializeRefObject(ar, "myScene", KAO2_E_SCENE_TYPEINFO)
        self._serializeRefObject(ar, "parentNode", KAO2_E_NODE_TYPEINFO)

        test = [1]
        ar.file.parseUInt32(test)

        self._serializeUInt32(ar, "collisionEntryId")

        self._serializeSerializables(ar, "axisList", KAO2_eAxisList, None, False)

        self._serializeUInt8Array(ar, "series", True)

        self._serializeRefObjectArray(ar, "unknown_80", KAO2_E_NODE_TYPEINFO)


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_ALBOX_TYPEINFO = KAO2_TypeInfo (
    0x01231325,
    "eALBox",
    KAO2_E_REFCOUNTER_TYPEINFO,
    lambda: KAO2_eALBox()
)


################################################################
