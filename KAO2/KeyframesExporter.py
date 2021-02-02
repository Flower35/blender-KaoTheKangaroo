################################################################
# "KAO2/KeyframesExporter.py"

import bpy
import traceback
import re
from bpy_extras.io_utils import ExportHelper
from mathutils import Matrix
from typing import List

from .Basic import (KAO2_ePoint3, KAO2_eQuat, KAO2_eSRP)
from ..KaoUtility import *


################################################################

class KAO2_ExportableXformKey(object):

    def __init__(self, time: float) -> None:

        self.time = time

        self.srp    = KAO2_eSRP()
        self.scale3 = KAO2_ePoint3(1, 1, 1)
        self.euler3 = KAO2_ePoint3(0, 0, 0)
        self.use_euler = 0

        self.flags = 0


################################################################

class KAO2_ExportableXform(object):

    def __init__(self, name: str) -> None:

        if re.search(r"\.[0-9]{3}$", name) is not None:
            self.name = name[:-4]
        else:
            self.name = name

        self.export_label = None

        self.children = []

        self.base_srp = KAO2_eSRP()

        key = KAO2_ExportableXformKey(-1)
        key.flags = 0x07
        self.keys = [key]

        self.animated = False

    def findByName(self, name: str) -> "KAO2_ExportableXform":

        if self.name == name:
            return self

        for child in self.children:
            test = child.findByName(name)
            if test is not None:
                return test

        return None

    def addKeys(self, path: str, index: int, keyframes: "bpy_prop_collection") -> None:

        _debug_header = "[KAO2] ExportableXform::addKeys({}):\n\t".format(self.name)
        prop_path = ""
        sign = +1
        use_euler = 0

        if "location" == path:
            if 0 == index:
                prop_path = "srp.pos.x"
            elif 1 == index:
                prop_path = "srp.pos.y"
            elif 2 == index:
                prop_path = "srp.pos.z"
            else:
                raise Exception(_debug_header + "Invalid \"location\" array index {}!".format(index))
            flag = 0x04

        elif "rotation_euler" == path:
            if 0 == index:
                prop_path = "euler3.x"
            elif 1 == index:
                prop_path = "euler3.y"
            elif 2 == index:
                prop_path = "euler3.z"
            else:
                raise Exception(_debug_header + "Invalid \"rotation_euler\" array index {}!".format(index))
            use_euler = +1
            flag = 0x02

        elif "rotation_quaternion" == path:
            if 0 == index:
                prop_path = "srp.rot.w"
            elif 1 == index:
                prop_path = "srp.rot.x"
                sign = -1
            elif 2 == index:
                prop_path = "srp.rot.y"
                sign = -1
            elif 3 == index:
                prop_path = "srp.rot.z"
                sign = -1
            else:
                raise Exception(_debug_header + "Invalid \"rotation_quaternion\" array index {}!".format(index))
            use_euler = -1
            flag = 0x02

        elif "scale" == path:
            if 0 == index:
                prop_path = "scale3.x"
            elif 1 == index:
                prop_path = "scale3.y"
            elif 2 == index:
                prop_path = "scale3.z"
            else:
                raise Exception(_debug_header + "Invalid \"scale\" array index {}!".format(index))
            flag = 0x01

        else:
            raise Exception(_debug_header + "Unknown data path \"{}\"!".format(path))

        prop_names = prop_path.split('.')
        last_name  = prop_names[-1]
        prop_names = prop_names[:-1]

        for src_key in keyframes:
            try:
                key = next(k for k in self.keys if src_key.co[0] == k.time)
            except StopIteration:
                key = None

            if key is None:
                key = KAO2_ExportableXformKey(src_key.co[0])
                self.keys.append(key)

            prop = key
            for name in prop_names:
                prop = getattr(prop, name)
            setattr(prop, last_name, sign * src_key.co[1])

            key.flags |= flag

            if 0 != use_euler:
                if 0 == key.use_euler:
                    key.use_euler = use_euler
                elif key.use_euler != use_euler:
                    raise Exception(_debug_header + "mixed \"rotation_euler\" with \"rotation_quaternion\"!")

        self.animated = True

    def mixWithBaseSRP(self) -> None:

        # Temporary keyframe: required if some bone has no keys defined,
        # otherwise it is removed from the list!
        if len(self.keys) > 1:
            del self.keys[0]
            self.keys[0].flags = 0x07
        else:
            self.keys[0].time = 0

        for k in self.keys:
            k.srp.scl = (k.scale3.x + k.scale3.y + k.scale3.z) / 3.0
            if k.use_euler > 0:
                k.srp.rot = KAO2_eQuat.fromEulerAngles(k.euler3.x, k.euler3.y, k.euler3.z)
            k.srp = KAO2_eSRP.mix(self.base_srp, k.srp)

        for child in self.children:
            child.mixWithBaseSRP()

    def writeIdentifiers(self, file: "_io.TextIoWrapper", ar_path: str, num_ref: List[int]) -> None:

        path = ar_path + self.name

        if self.animated:
            self.export_label = "xform{:03d}".format(num_ref[0])
            num_ref[0] += 1

            file.write("    FindNode eTransform {} (\"{}\")\n".format(self.export_label, path))

        for child in self.children:
            child.writeIdentifiers(file, path + "/", num_ref)

    def writeKeyframes(self, file: "_io.TextIoWrapper") -> None:

        if self.animated:
            file.write("    NodeMsg {} ctrlClearKeyframes(-1)\n".format(self.export_label))

            for k in self.keys:
                file.write (
                    "    NodeMsg {} ctrlAddKeyframe(-1 {:.0f} [{:.12f} {:.12f} {:.12f}] [{:.12f} {:.12f} {:.12f} {:.12f}] [{:.12f}] {:1d})\n".format (
                        self.export_label,
                        k.time,
                        k.srp.pos.x, k.srp.pos.y, k.srp.pos.z,
                        k.srp.rot.x, k.srp.rot.y, k.srp.rot.z,  k.srp.rot.w,
                        k.srp.scl,
                        k.flags ))

            file.write("\n")

        for child in self.children:
            child.writeKeyframes(file)


################################################################

class KAO2_BoneHierarchy():

    def __init__(self, editbone: "bpy_types.EditBone") -> None:

        self.editbone = editbone
        if editbone is None:
            self.name = ""
            self.world_matrix = Matrix()
        else:
            self.name = editbone.name
            self.world_matrix = editbone.matrix
        self.children = []

    def appendBone(self, other: "KAO2_BoneHierarchy") -> bool:

        if (other.editbone.parent is None) or (other.editbone.parent == self.editbone):
            self.children.append(other)
            return True

        else:
            for child in self.children:
                if child.appendBone(other):
                    return True

        return False

    def toXformList(self, parent: "KAO2_BoneHierarchy") -> KAO2_ExportableXform:

        result = KAO2_ExportableXform(self.name)

        if parent is not None:
            m = parent.world_matrix.inverted() @ self.world_matrix
        else:
            m = self.world_matrix

        pos, rot, _ = m.decompose()

        result.base_srp.pos = KAO2_ePoint3(pos.x, pos.y, pos.z)
        result.base_srp.rot = KAO2_eQuat(- rot.x, - rot.y, - rot.z, rot.w)

        result.animated = True

        for child in self.children:
            result.children.append(child.toXformList(self))

        return result


################################################################

def _kfexp_prepare_objects(obj) -> KAO2_ExportableXform:

    _debug_header = "[KAO2] KeyframesExporter(\"{}\"):\n\t".format(obj.name)

    result = KAO2_ExportableXform(obj.name)

    if (obj.animation_data is not None) and (obj.animation_data.action is not None):

        anim = obj.animation_data.action

        if "ARMATURE" == obj.type:

            # dummy root for EditBones
            hierarchy = KAO2_BoneHierarchy(None)

            last_obj, last_mode = push_active_obj()
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode = "EDIT")

            for bone in obj.data.edit_bones:
                hierarchy.appendBone(KAO2_BoneHierarchy(bone))

            pop_active_obj(last_obj, last_mode)

            # Building a tree of xforms
            hierarchy2 = hierarchy.toXformList(None)
            result.children.extend(hierarchy2.children)

        for f in anim.fcurves:

            if f.data_path.startswith("pose.bones[\""):
                name_end = f.data_path.rfind("\"].")
                if name_end > 12:
                    bone_name = f.data_path[12:name_end]
                    xform = hierarchy2.findByName(bone_name)
                    if xform is not None:
                        xform.addKeys(f.data_path[name_end + 3 :], f.array_index, f.keyframe_points)
                    else:
                        raise Exception (_debug_header + "Bone \"{}\" not found!".format(bone_name))
                else:
                    raise Exception (_debug_header + "Bone not found in \"fcurve.data_path\"".format())

            else:
                result.addKeys(f.data_path, f.array_index, f.keyframe_points)

    for child in obj.children:
        test = _kfexp_prepare_objects(child)
        result.children.append(test)

    return result


################################################################

class BLENDER_OT_KAO2_KeyframesExporter(bpy.types.Operator, ExportHelper):
    """Export keyframes of selected armature into a text format importable in ZookieWizard."""
    bl_idname = "kao_the_kangaroo_round_2.export_keyframes"
    bl_label = "Export Keyframes"

    filename_ext = ".log"
    filter_glob: bpy.props.StringProperty (
        default = "*.log",
        options = {"HIDDEN"},
        maxlen = 255
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        try:
            with open(self.filepath, "w") as file:

                _debug_header = "[KAO2] KeyframesExporter(\"{}\"):\n\t".format(context.active_object.name)

                print("-" * 64)
                print(_debug_header + "Converting animation data...")

                xforms_root = _kfexp_prepare_objects(context.active_object)

                # Elephant Engine requires transformations to be relative to parent bone,
                # no concept of a default rig pose, as opposed to "EditBones" in Blender.
                # This function runs recursively, that is why it is called after preparations.
                xforms_root.mixWithBaseSRP()

                print(_debug_header + "Saving text instructions...")

                file.write("/*\n    ZookieWizard instructions.\n*/\n\n")
                bone_num = [0]
                xforms_root.writeIdentifiers(file, "/*/", bone_num)
                file.write("\n")

                xforms_root.writeKeyframes(file)

            text = "Keyframes exporting success!"
            self.report({"INFO"}, text)
            print("-" * 64)
            print("[KAO2] " + text)

            return {"FINISHED"}

        except Exception as e:

            traceback.print_exc()
            self.report({"ERROR"}, str(e))

            return {"CANCELLED"}


################################################################
