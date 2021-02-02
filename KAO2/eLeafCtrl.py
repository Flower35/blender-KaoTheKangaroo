################################################################
# "KAO2/eLeafCtrl.py"

import bpy
from typing import List

from .Basic import (KAO2_Serializable, KAO2_ePoint1, KAO2_ePoint3, KAO2_eQuat, KAO2_eSRP)
from .eCtrl import (KAO2_eCtrl, KAO2_E_CTRL_FLOAT_TYPEINFO, KAO2_E_CTRL_POINT3_TYPEINFO, KAO2_E_CTRL_QUAT_TYPEINFO)


class KAO2_eLeafKey(KAO2_Serializable):

    def __init__(self, subclass_type: type) -> None:

        if subclass_type not in (KAO2_ePoint1, KAO2_ePoint3, KAO2_eQuat):
            raise Exception("[KAO2] eLeafKey::__init__():\n\t" + "Invalid subclass type!")

        self._subclass_type = subclass_type

        self.time = 0
        self.data = [None] * 3

    def serialize(self, ar: "KAO2_Archive") -> None:

        self._serializeFloat(ar, "time")
        self._serializeSerializables(ar, "data", self._subclass_type, None, False)


class KAO2_eLeafCtrl(KAO2_eCtrl):

    def __init__(self, subclass_type: type) -> None:

        KAO2_eCtrl.__init__(self, subclass_type)

        self.outOfRangeType = [0, 0]
        self.keys = []
        self.defaultKey = self._subclass_type()

    def getType(self) -> "KAO2_TypeInfo":

        if KAO2_ePoint1 is self._subclass_type:
            return KAO2_E_LEAFCTRL_FLOAT_TYPEINFO

        elif KAO2_ePoint3 is self._subclass_type:
            return KAO2_E_LEAFCTRL_POINT3_TYPEINFO

        elif KAO2_eQuat is self._subclass_type:
            return KAO2_E_LEAFCTRL_QUAT_TYPEINFO

        return None

    def serialize(self, ar: "KAO2_Archive") -> None:

        assert 2 == len(self.outOfRangeType)
        self._serializeUInt32Array(ar, "outOfRangeType", False)

        self._serializeSerializables(ar, "keys", KAO2_eLeafKey, self._subclass_type, True)

        self.defaultKey.serialize(ar)

    def ctrlGenerateBlenderFCurves(self, anim_id: int, bone_name: str) -> None:

        raise Exception("[KAO2] eLeafCtrl::ctrlGenerateBlenderFCurves():\n\t" + "OUT OF CONTEXT!")

    def ctrlCollectKeyframes(self, index: int, curves: List[bpy.types.FCurve]) -> None:

        key_count = len(self.keys)
        keys_to_add = 1 if (key_count <= 0) else key_count

        if KAO2_ePoint1 is self._subclass_type:
            curves[index].keyframe_points.add(keys_to_add)
            if key_count <= 0:
                curves[index].keyframe_points[0].co = [0, self.defaultKey.x]
                curves[index].keyframe_points[0].interpolation = "CONSTANT"
            else:
                for k in range (0, key_count):
                    curves[index].keyframe_points[k].co = [self.keys[k].time, self.keys[k].data[0].x]
                    curves[index].keyframe_points[k].interpolation = "CUBIC"

        elif KAO2_ePoint3 is self._subclass_type:
            curves[0].keyframe_points.add(keys_to_add)
            curves[1].keyframe_points.add(keys_to_add)
            curves[2].keyframe_points.add(keys_to_add)
            if key_count <= 0:
                curves[0].keyframe_points[0].co = [0, self.defaultKey.x]
                curves[0].keyframe_points[0].interpolation = "CONSTANT"
                curves[1].keyframe_points[0].co = [0, self.defaultKey.y]
                curves[1].keyframe_points[0].interpolation = "CONSTANT"
                curves[2].keyframe_points[0].co = [0, self.defaultKey.z]
                curves[2].keyframe_points[0].interpolation = "CONSTANT"
            else:
                for k in range (0, key_count):
                    curves[0].keyframe_points[k].co = [self.keys[k].time, self.keys[k].data[0].x]
                    curves[0].keyframe_points[k].interpolation = "CUBIC"
                    curves[1].keyframe_points[k].co = [self.keys[k].time, self.keys[k].data[0].y]
                    curves[1].keyframe_points[k].interpolation = "CUBIC"
                    curves[2].keyframe_points[k].co = [self.keys[k].time, self.keys[k].data[0].z]
                    curves[2].keyframe_points[k].interpolation = "CUBIC"

        elif KAO2_eQuat is self._subclass_type:
            curves[0].keyframe_points.add(keys_to_add)
            curves[1].keyframe_points.add(keys_to_add)
            curves[2].keyframe_points.add(keys_to_add)
            curves[3].keyframe_points.add(keys_to_add)
            if key_count <= 0:
                curves[0].keyframe_points[0].co = [0, self.defaultKey.w]
                curves[0].keyframe_points[0].interpolation = "CONSTANT"
                curves[1].keyframe_points[0].co = [0, - self.defaultKey.x]
                curves[1].keyframe_points[0].interpolation = "CONSTANT"
                curves[2].keyframe_points[0].co = [0, - self.defaultKey.y]
                curves[2].keyframe_points[0].interpolation = "CONSTANT"
                curves[3].keyframe_points[0].co = [0, - self.defaultKey.z]
                curves[3].keyframe_points[0].interpolation = "CONSTANT"
            else:
                for k in range (0, key_count):
                    curves[0].keyframe_points[k].co = [self.keys[k].time, self.keys[k].data[0].w]
                    curves[0].keyframe_points[k].interpolation = "CUBIC"
                    curves[1].keyframe_points[k].co = [self.keys[k].time, - self.keys[k].data[0].x]
                    curves[1].keyframe_points[k].interpolation = "CUBIC"
                    curves[2].keyframe_points[k].co = [self.keys[k].time, - self.keys[k].data[0].y]
                    curves[2].keyframe_points[k].interpolation = "CUBIC"
                    curves[3].keyframe_points[k].co = [self.keys[k].time, - self.keys[k].data[0].z]
                    curves[3].keyframe_points[k].interpolation = "CUBIC"

        else:
            raise Exception("eLeafCtrl::ctrlCollectKeyframes():\n\t" + "OUT OF CONTEXT!")


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_LEAFCTRL_FLOAT_TYPEINFO = KAO2_TypeInfo (
    0xA001,
    "eLeafCtrl<eFloatKey>",
    KAO2_E_CTRL_FLOAT_TYPEINFO,
    lambda: KAO2_eLeafCtrl(KAO2_ePoint1)
)

KAO2_E_LEAFCTRL_POINT3_TYPEINFO = KAO2_TypeInfo (
    0xA002,
    "eLeafCtrl<ePoint3Key>",
    KAO2_E_CTRL_POINT3_TYPEINFO,
    lambda: KAO2_eLeafCtrl(KAO2_ePoint3)
)

KAO2_E_LEAFCTRL_QUAT_TYPEINFO = KAO2_TypeInfo (
    0xA003,
    "eLeafCtrl<eRotationKey>",
    KAO2_E_CTRL_QUAT_TYPEINFO,
    lambda: KAO2_eLeafCtrl(KAO2_eQuat)
)


################################################################
