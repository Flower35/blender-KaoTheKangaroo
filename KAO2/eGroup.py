################################################################
# "KAO2/eGroup.py"

import bpy
from mathutils import Vector, Quaternion, Matrix

from ..KaoUtility import *

from .Basic import KAO2_eSRP

from .eNode import (KAO2_eNode, KAO2_E_NODE_TYPEINFO)

class KAO2_eGroup(KAO2_eNode):

    GROUP_SPECIAL_TYPE_NONE = 0
    GROUP_SPECIAL_TYPE_ARMATURE = 1
    GROUP_SPECIAL_TYPE_JOINT = 2

    def __init__(self) -> None:

        KAO2_eNode.__init__(self)

        self.nodes = []
        self.groupType = KAO2_eGroup.GROUP_SPECIAL_TYPE_NONE
        self.boneName = ""

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_GROUP_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        KAO2_eNode.serialize(self, ar)

        self._serializeRefObjectArray(ar, "nodes", KAO2_E_NODE_TYPEINFO)

    def toBlenderObject(self) -> bpy.types.Object:

        # Note: "blenderObj" shall NOT exist for "GROUP_SPECIAL_TYPE_JOINT"
        if self.blenderObj is not None:
            return self.blenderObj

        _debug_header = "[KAO2] eGroup::toBlenderObject():\n\t"

        arm_obj = Settings.armatureParent

        # Create Armature data block before creating the main Object
        if KAO2_eGroup.GROUP_SPECIAL_TYPE_ARMATURE == self.groupType:

            if Settings.blenderObjData is not None:
                raise Exception(_debug_header + "NOT SUPPORTED SETTING!")

            Settings.blenderObjData = bpy.data.armatures.new(name = self.name.text)
            Settings.blenderObjData.display_type = "STICK"

            if Settings.ignoreRestPoseUseShapeKeys:
                previous_armature_xforms = Settings.armatureBoneXforms
                previous_armature_meshes = Settings.armatureModifiedMeshes

        # Create the main object
        if KAO2_eGroup.GROUP_SPECIAL_TYPE_JOINT != self.groupType:
            obj = KAO2_eNode.toBlenderObject(self)
        else:
            obj = None
            if not self.boneName:
                raise Exception(_debug_header + "Bone name is missing! (me: \"{}\")".format(self.name.text))
        Settings.blenderObjData = None

        # Remember the current Armature Parent
        if KAO2_eGroup.GROUP_SPECIAL_TYPE_ARMATURE == self.groupType:
            Settings.armatureParent = obj

            # Blender context workaround (object must be visible)
            # (adding bones in "EDIT" mode)
            bpy.context.collection.objects.link(obj)

        # Convert every child node
        for node in self.nodes:
            test = node.toBlenderObject()

            if KAO2_eGroup.GROUP_SPECIAL_TYPE_ARMATURE == self.groupType:

                if node.getType().checkHierarchy(KAO2_E_GROUP_TYPEINFO):

                    # Currently do nothing special with a Root Bone
                    if KAO2_eGroup.GROUP_SPECIAL_TYPE_JOINT == node.groupType:
                        pass

                    # Attach a regular group to this armature
                    elif KAO2_eGroup.GROUP_SPECIAL_TYPE_NONE == node.groupType:
                        node.rigToBlenderArmature(obj, "")

                    else:
                        raise Exception(_debug_header + "NOT SUPPORTED SETTING!")

                else:

                    # Attach a regular node to this armature
                    node.rigToBlenderArmature(obj, "")

            elif KAO2_eGroup.GROUP_SPECIAL_TYPE_JOINT == self.groupType:

                if arm_obj is None:
                    raise Exception(_debug_header + "Armature is missing!")

                if node.getType().checkHierarchy(KAO2_E_GROUP_TYPEINFO):

                    # Attach a child bone to this bone
                    if KAO2_eGroup.GROUP_SPECIAL_TYPE_JOINT == node.groupType:

                        KAO2_eGroup.linkBonesUnderArmature(arm_obj, self.boneName, node.boneName)

                    # Converting some lose groups that are not bones, but have some children bones
                    elif node.jointCandidate and (KAO2_eGroup.GROUP_SPECIAL_TYPE_ARMATURE != node.groupType):

                        node.createBoneInArmature(arm_obj, (0, 0, 0), (1, 0, 0, 0), (1, 1, 1))

                    # Attach a regular group (or sub-armature) to this bone
                    else:

                        node.rigToBlenderArmature(arm_obj, self.boneName)

                else:

                    # Attach a regular node to this bone
                    node.rigToBlenderArmature(arm_obj, self.boneName)

            else:

                if test is None:
                    test = "" if (node is None) else node.name.text
                    raise Exception(_debug_header + "Blender object is missing for node \"{}\")!\n\t".format(test) + "(me: \"{}\", jointCandidate: {}, groupType: {})".format(self.name.text, self.jointCandidate, self.groupType))
                test.parent = obj

        # Leaving the current armature
        if Settings.armatureParent is obj:
            last_obj, last_mode = push_active_obj()

            # Applying the current pose as a new bind pose
            # (all joints were placed at [0,0,0] by default)
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode = "POSE")
            bpy.ops.pose.armature_apply(selected = False)

            if Settings.ignoreRestPoseUseShapeKeys:

                print("-" * 64)
                print(_debug_header + "Inverting bones transformations in \"POSE MODE\", applying shape modifiers to some meshes...")

                # Pairs of [bone name, KAO2_eSRP]
                for xform in Settings.armatureBoneXforms:
                    bone = obj.pose.bones.get(xform[0])
                    if bone is None:
                        raise Exception(_debug_header + "Pose Bone \"{}\" not found. (Armature: \"{}\")".format(xform[0], obj.name))

                    pos, rot, scl = Matrix(xform[1].getInverseMatrix().m).decompose()
                    bone.location = pos
                    bone.rotation_quaternion = rot
                    bone.scale = scl

                for mesh in Settings.armatureModifiedMeshes:

                    modifier = mesh.modifiers.new(name = "", type = "ARMATURE")
                    modifier.object = obj

                    # Blender context workaround (object must be visible)
                    # (applying a poor quality modifier as SHAPE KEY)
                    bpy.context.collection.objects.link(mesh)

                    bpy.context.view_layer.objects.active = mesh
                    bpy.ops.object.modifier_apply(apply_as = "SHAPE", modifier = modifier.name)
                    mesh.data.shape_keys.key_blocks[1].value = 1.0
                    obj.active_shape_key_index = 1

                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode = "POSE")
                bpy.ops.pose.armature_apply(selected = False)

                Settings.armatureBoneXforms = previous_armature_xforms
                Settings.armatureModifiedMeshes = previous_armature_meshes

            pop_active_obj(last_obj, last_mode)

        Settings.armatureParent = arm_obj

        return obj

    def createBoneInArmature(self, armature_parent: bpy.types.Object, pos: Vector, rot: Quaternion, scl: Vector) -> None:

        _debug_header = "[KAO2] eGroup::createBoneInArmature():\n\t"

        print("-" * 64)
        print(_debug_header[:-2] + " \"{}\"".format(self.name.text))

        last_obj, last_mode = push_active_obj()

        bpy.context.view_layer.objects.active = armature_parent
        bpy.ops.object.mode_set(mode = "EDIT")

        bone = armature_parent.data.edit_bones.new(name = self.name.text)
        if bone is None:
            raise Exception(_debug_header + "Failed to create an EditBone \"{}\" for Armature \"{}\".".format(self.name.text, armature_parent.name))
        self.boneName = bone.name

        bone.head = [0, 0, 0]
        bone.tail = [0, 1.0, 0]

        bone.use_connect = False
        bone.use_local_location = True
        bone.use_deform = True

        bpy.ops.object.mode_set(mode = "POSE")

        bone = armature_parent.pose.bones.get(self.boneName)
        if bone is None:
            raise Exception(_debug_header + "Pose Bone \"{}\" not found. THIS SHOULD NEVER HAPPEN !!!".format(self.boneName))

        bone.location = pos
        bone.rotation_quaternion = rot
        bone.scale = scl

        pop_active_obj(last_obj, last_mode)

        if Settings.ignoreRestPoseUseShapeKeys:
            Settings.armatureBoneXforms.append([self.boneName, self.defaultTransform])

        # In case this node only has the "jointCandidate" property
        self.groupType = KAO2_eGroup.GROUP_SPECIAL_TYPE_JOINT

    @staticmethod
    def linkBonesUnderArmature(armature_parent: bpy.types.Object, parent_bone_name: str, child_bone_name: str) -> None:

        _debug_header = "[KAO2] eGroup::linkBonesUnderArmature():\n\t"

        last_obj, last_mode = push_active_obj()

        bpy.context.view_layer.objects.active = armature_parent
        bpy.ops.object.mode_set(mode = "EDIT")

        parent_bone = armature_parent.data.edit_bones.get(parent_bone_name)
        if parent_bone is None:
            raise Exception(_debug_header + "Parent Bone is missing!")

        child_bone = armature_parent.data.edit_bones.get(child_bone_name)
        if child_bone is None:
            raise Exception(_debug_header + "Child Bone is missing")

        child_bone.parent = parent_bone

        pop_active_obj(last_obj, last_mode)

    def rigToBlenderArmature(self, armature_parent: bpy.types.Object, bone_name: str) -> None:

        obj = self.blenderObj
        if obj is None:
            raise Exception("[KAO2] eGroup::rigToBlenderArmature():\n\t" + "Blender object is missing!")

        if obj.parent is None:
            obj.parent = armature_parent

            if bone_name:
                # Workaround for `bpy.ops.pose.armature_apply()`
                # (recalculating object's local transformation)
                if obj.name not in bpy.context.collection.objects:
                    bpy.context.collection.objects.link(obj)

                obj.parent_type = "BONE"
                obj.parent_bone = bone_name

        if KAO2_eGroup.GROUP_SPECIAL_TYPE_ARMATURE != self.groupType:
            for node in self.nodes:
                node.rigToBlenderArmature(armature_parent, None)

    def updateBlenderAnims(self) -> None:

        obj = self.blenderObj
        arm_obj = Settings.armatureParent

        if KAO2_eGroup.GROUP_SPECIAL_TYPE_ARMATURE == self.groupType:
            Settings.armatureParent = obj

            if len(Settings.actionsList) > 0:
                if not obj.animation_data:
                    obj.animation_data_create()
                obj.animation_data.action = Settings.actionsList[0]

        for node in self.nodes:
            node.updateBlenderAnims()

        Settings.armatureParent = arm_obj


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_GROUP_TYPEINFO = KAO2_TypeInfo (
    0x8111,
    "eGroup",
    KAO2_E_NODE_TYPEINFO,
    lambda: KAO2_eGroup()
)

from .eString import KAO2_eString


################################################################
