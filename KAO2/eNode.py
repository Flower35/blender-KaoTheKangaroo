################################################################
# "KAO2/eNode.py"

import bpy

from ..KaoUtility import *

from .Basic import KAO2_eSRP

from .eRefCounter import (KAO2_eRefCounter, KAO2_E_REFCOUNTER_TYPEINFO)

class KAO2_eNode(KAO2_eRefCounter):

    def __init__(self) -> None:

        self.previousTransform = None
        self.unknown_0C = 0x00FFFFFF
        self.parent = None
        self.name = KAO2_eString()
        self.axisListBox = None
        self.flags = 0x249D
        self.collisionFlags = 0x00FF
        self.visCtrl = None
        self.sphBound = [0, 0, 0, (-1)]
        self.visGroup = (-1)

        self.blenderObj = None
        self.jointCandidate = False

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_NODE_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        if ar.version < 0x82:
            raise Exception("[KAO2] eNode::serialize():\n\t" + "ar.version() 130 required!")

        self._serializeString(ar, "name")

        from .eGroup import KAO2_E_GROUP_TYPEINFO
        self._serializeRefObject(ar, "parent", KAO2_E_GROUP_TYPEINFO)

        self._serializeUInt32(ar, "unknown_0C")

        self._serializeRefObject(ar, "axisListBox", KAO2_E_ALBOX_TYPEINFO)

        self._serializeUInt32(ar, "flags")

        assert 4 == len(self.sphBound)
        self._serializeFloatArray(ar, "sphBound", False)

        self._serializeRefObject(ar, "visCtrl", KAO2_E_CTRL_FLOAT_TYPEINFO)

        self._serializeUInt16(ar, "collisionFlags")

        if ar.version < 0x8D:

            self.visGroup = (-1)

        else:

            test = [self.visGroup]

            if ar.version < 0x90:

                ar.file.parseInt16(test)

            else:

                ar.file.parseInt32(test)

            self.visGroup = test[0]

        if ar.isInReadMode:

            self.flags |= 0x00002000

    def getLastSRP(self, world: bool) -> KAO2_eSRP:

        from .eTransform import KAO2_E_TRANSFORM_TYPEINFO

        test = self.parent
        while test is not None:
            if test.getType().checkHierarchy(KAO2_E_TRANSFORM_TYPEINFO):
                return test.worldTransform if world else test.defaultTransform
            test = test.parent

        return KAO2_eSRP()

    def toBlenderObject(self) -> bpy.types.Object:

        if self.blenderObj is not None:
            return self.blenderObj

        _debug_header = "[KAO2] eNode::toBlenderObject():\n\t"

        print("-" * 64)
        print(_debug_header[:-2] + " \"{}\"".format(self.name.text))

        if self.visCtrl is not None:
            print(_debug_header + "\"{}\" uses Visibility controller.".format(self.name.text))

        obj = bpy.data.objects.new(name = self.name.text, object_data = Settings.blenderObjData)

        obj.location = Settings.blenderObjTransform[0]
        obj.rotation_mode = "QUATERNION"
        obj.rotation_quaternion = Settings.blenderObjTransform[1]
        obj.scale = Settings.blenderObjTransform[2]
        Settings.blenderObjTransform = [(0, 0, 0), (1, 0, 0, 0), (1, 1, 1)]

        # TODO: zachować pozostałe parametry, jak flagi, visCtrl, itp. (!!!)

        self.blenderObj = obj
        return obj

    def rigToBlenderArmature(self, armature_parent: bpy.types.Object, bone_name: str) -> None:

        raise Exception("[KAO2] eNode::rigToBlenderArmature():\n\t" + "NOT SUPPORTED!")

    def updateBlenderAnims(self) -> None:

        pass


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_NODE_TYPEINFO = KAO2_TypeInfo (
    0x8000,
    "eNode",
    KAO2_E_REFCOUNTER_TYPEINFO,
    lambda: KAO2_eNode()
)

from .eString import KAO2_eString

from .eALBox import KAO2_E_ALBOX_TYPEINFO
from .eCtrl import KAO2_E_CTRL_FLOAT_TYPEINFO


################################################################
