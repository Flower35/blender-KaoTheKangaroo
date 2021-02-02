################################################################
# "KAO2/eTransform.py"

import bpy
from mathutils import Matrix

from ..KaoUtility import *

from .eGroup import (KAO2_eGroup, KAO2_E_GROUP_TYPEINFO)

class KAO2_eTransform(KAO2_eGroup):

    def __init__(self) -> None:

        KAO2_eGroup.__init__(self)

        self.defaultTransform = KAO2_eSRP()
        self.worldTransform = KAO2_eSRP()
        self.ctrl = None

        self.invBindMatrix = None

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_TRANSFORM_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        KAO2_eGroup.serialize(self, ar)

        self.defaultTransform.serialize(ar)
        self.worldTransform.serialize(ar)
        self._serializeRefObject(ar, "ctrl", KAO2_E_CTRL_SRP_TYPEINFO)

    def markAsJoint(self, inv_bind_mat: "KAO2_eMatrix4x4") -> None:

        if Settings.ignoreInvBindMatrices:
            if self.invBindMatrix is not None:
                if self.invBindMatrix != inv_bind_mat:
                    print("[KAO2] eTransform::markAsJoint():\n\t" + "WARNING! Inverse Bind Matrices are different! (\"{}\")\n".format(self.name.text) + str(self.invBindMatrix.m) + "\n" + str(inv_bind_mat.m))

            self.invBindMatrix = inv_bind_mat

        self.groupType = KAO2_eGroup.GROUP_SPECIAL_TYPE_JOINT

    def toBlenderObject(self) -> bpy.types.Object:

        if self.blenderObj is not None:
            return self.blenderObj

        _debug_header = "[KAO2] eTransform::toBlenderObject():\n\t"

        print("-" * 64)
        print(_debug_header[:-2] + " \"{}\"".format(self.name.text))

        if self.ctrl is not None:
            print(_debug_header + "\"{}\" uses SRP controller.".format(self.name.text))

        arm_obj = Settings.armatureParent
        if (KAO2_eGroup.GROUP_SPECIAL_TYPE_JOINT == self.groupType) and (arm_obj is None):
            raise Exception(_debug_header + "Armature parent is missing!")

        # Store current World Matrix
        world_matrix = KAO2_eMatrix4x4(Settings.worldMatrix)

        if self.invBindMatrix is not None:

            local_matrix = KAO2_eMatrix4x4()
            local_matrix.fromBlenderMatrix(Matrix(world_matrix.m).inverted() @ Matrix(self.invBindMatrix.m).inverted())

            # Save bone's Bind Pose as a local transformation
            pos, rot, scl = self.defaultTransform.fromMatrix(local_matrix)

            self.invBindMatrix = None

        else:

            scl, rot, pos = self.defaultTransform.toBlenderVectors()

            local_matrix = self.defaultTransform.getMatrix()

        # Extend current World Matrix (for children transforms)
        Settings.worldMatrix = (world_matrix @ local_matrix).m

        if (arm_obj is None) or (KAO2_eGroup.GROUP_SPECIAL_TYPE_ARMATURE == self.groupType) or ((not self.jointCandidate) and (KAO2_eGroup.GROUP_SPECIAL_TYPE_JOINT != self.groupType) and (self.ctrl is None)):

            Settings.blenderObjTransform[0] = pos
            Settings.blenderObjTransform[1] = rot
            Settings.blenderObjTransform[2] = scl

        else:

            self.createBoneInArmature(arm_obj, pos, rot, scl)

        obj = KAO2_eGroup.toBlenderObject(self)

        # Restore previous World Matrix
        Settings.worldMatrix = world_matrix.m

        return obj

    def rigToBlenderArmature(self, armature_parent: bpy.types.Object, bone_name: str) -> None:

        if KAO2_eGroup.GROUP_SPECIAL_TYPE_JOINT == self.groupType:
            raise Exception("[KAO2] eTransform::rigToBlenderArmature():\n\t" + "NOT SUPPORTED SETTING! (me: \"{}\", passed bone name: \"{}\")".format(self.name.text, str(bone_name)))
        else:
            KAO2_eGroup.rigToBlenderArmature(self, armature_parent, bone_name)

    def updateBlenderAnims(self) -> None:

        _debug_header = "[KAO2] eTransform::updateBlenderAnims():\n\t"

        previous_actions = Settings.actionsList
        restore_actions = (KAO2_eGroup.GROUP_SPECIAL_TYPE_ARMATURE != self.groupType)

        if self.ctrl is not None:

            # Creating independent actions for this xform.
            if not self.boneName:
                Settings.actionsList = []

                obj = self.blenderObj
                if obj is None:
                    raise Exception(_debug_header + "Blender object is missing!")

                if self.ctrl.getType() is KAO2_E_SRPCOMBINECTRL_TYPEINFO:

                    if not restore_actions:
                        raise Exception(_debug_header + "NOT SUPPORTED SETTING!")

                    action = bpy.data.actions.new(name = "Unnamed track ({})".format(self.name.text))
                    action.use_fake_user = True
                    Settings.actionsList.append(action)
                else:
                    for i in range (0, len(previous_actions)):
                        action = bpy.data.actions.new(name = previous_actions[i].name + " ({})".format(self.name.text))
                        action.use_fake_user = True
                        Settings.actionsList.append(action)

                if len(Settings.actionsList) > 0:
                    if not obj.animation_data:
                        obj.animation_data_create()
                    obj.animation_data.action = Settings.actionsList[0]

            self.ctrl.ctrlGenerateBlenderFCurves(0, self.boneName)

            # Restoring bone's Bind Pose
            if self.boneName:
                arm_obj = Settings.armatureParent
                if arm_obj is None:
                    raise Exception(_debug_header + "Armature parent is missing!")

                last_obj, last_mode = push_active_obj()
                bpy.context.view_layer.objects.active = arm_obj
                bpy.ops.object.mode_set(mode = "POSE")

                bone = arm_obj.pose.bones.get(self.boneName)
                if bone is None:
                    raise Exception(_debug_header + "Pose Bone \"{}\" not found. THIS SHOULD NEVER HAPPEN !!!".format(self.boneName))

                bone.location = [0, 0, 0]
                bone.rotation_quaternion = [1, 0, 0, 0]
                bone.scale = [1, 1, 1]

                pop_active_obj(last_obj, last_mode)

        if restore_actions:
            Settings.actionsList = previous_actions

        KAO2_eGroup.updateBlenderAnims(self)

        if not restore_actions:
            Settings.actionsList = previous_actions


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_TRANSFORM_TYPEINFO = KAO2_TypeInfo (
    0x8112,
    "eTransform",
    KAO2_E_GROUP_TYPEINFO,
    lambda: KAO2_eTransform()
)

from .Basic import (KAO2_ePoint3, KAO2_ePoint4, KAO2_eMatrix4x4, KAO2_eSRP)
from .eCtrl import KAO2_E_CTRL_SRP_TYPEINFO
from .eSRPCombineCtrl import KAO2_E_SRPCOMBINECTRL_TYPEINFO


################################################################
