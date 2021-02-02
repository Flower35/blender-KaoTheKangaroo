################################################################
# "KAO2/eCamera.py"

import bpy
from math import radians

from ..KaoUtility import *

from .eTransform import (KAO2_eTransform, KAO2_E_TRANSFORM_TYPEINFO)

class KAO2_eCamera(KAO2_eTransform):

    def __init__(self) -> None:

        KAO2_eTransform.__init__(self)

        self.pathCtrl = None
        self.unknown_0150 = 0x00
        self.unknown_0151 = 0x00
        self.unknown_0154 = [200.0, (-200.0), (-200.0), 200.0]
        self.fov = 75.0
        self.nearPlane = 32.0
        self.farPlane = 220000.0
        self.look = [[0, 1.0, 0], [0, 0, 1.0], [1.0, 0, 0]]
        self.unknown_0194 = 0
        self.unknown_0198 = 0
        self.followCurrentActor = True
        self.camTarget = None
        self.unknown_01D8_A = 80.0
        self.unknown_01D8_B = 600.0
        self.unknown_01D8_C = 0
        self.unknown_01D8_D = 200.0

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_CAMERA_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        KAO2_eNode.serialize(self, ar)

        self.defaultTransform.serialize(ar)
        self.worldTransform.serialize(ar)
        self._serializeRefObject(ar, "ctrl", KAO2_E_CTRL_SRP_TYPEINFO)

        self._serializeUInt8(ar, "unknown_0151")

        assert 4 == len(self.unknown_0154)
        self._serializeFloatArray(ar, "unknown_0154", False)

        self._serializeFloat(ar, "fov")
        self._serializeFloat(ar, "nearPlane")
        self._serializeFloat(ar, "farPlane")

        for i in range(0, 3):
            for j in range (0, 3):
                ar.file.parseFloat(self.look[i], j)

        self._serializeFloat(ar, "unknown_0194")
        self._serializeFloat(ar, "unknown_0198")
        self._serializeUInt8(ar, "unknown_0150")

        self._serializeRefObject(ar, "pathCtrl", KAO2_E_PATHCAMCTRL_TYPEINFO)

        self._serializeRefObject(ar, "camTarget", KAO2_E_TRANSFORM_TYPEINFO)

        test = [1]
        ar.file.parseUInt32(test)
        if 1 != test[0]:
            raise Exception("[KAO2] eCamera::serialize():\n\t" + "non-empty member is not supported!")

        self._serializeFloat(ar, "unknown_01D8_B")
        self._serializeFloat(ar, "unknown_01D8_D")
        self._serializeFloat(ar, "unknown_01D8_A")
        self._serializeFloat(ar, "unknown_01D8_C")

        self._serializeUInt8(ar, "followCurrentActor")

    def toBlenderObject(self) -> bpy.types.Object:

        if self.blenderObj is not None:
            return self.blenderObj

        if (Settings.blenderObjData is not None) or (KAO2_eGroup.GROUP_SPECIAL_TYPE_NONE != self.groupType):
            raise Exception("[KAO2] eCamera::toBlenderObject():\n\t" + "NOT SUPPORTED SETTING!")
        cam = bpy.data.cameras.new(name = self.name.text)

        Settings.blenderObjData = cam
        obj = KAO2_eTransform.toBlenderObject(self)
        Settings.blenderObjData = None

        if self.camTarget is not None:
            co = obj.constraints.new("TRACK_TO")
            co.target = self.camTarget.toBlenderObject()
            co.up_axis = "UP_Y"
            co.track_axis = "TRACK_NEGATIVE_Z"

        cam.clip_end = 5000.0
        cam.angle = radians(self.fov)

        return obj


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_CAMERA_TYPEINFO = KAO2_TypeInfo (
    0x0CA4E7A1,
    "eCamera",
    KAO2_E_TRANSFORM_TYPEINFO,
    lambda: KAO2_eCamera()
)

from .eNode import KAO2_eNode
from .eGroup import KAO2_eGroup
from .eCtrl import KAO2_E_CTRL_SRP_TYPEINFO
from .ePathCamCtrl import KAO2_E_PATHCAMCTRL_TYPEINFO


################################################################
