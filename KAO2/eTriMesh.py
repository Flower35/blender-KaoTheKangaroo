################################################################
# "KAO2/eTriMesh.py"

import bpy

from ..KaoUtility import *

from .eGeometry import (KAO2_eGeometry, KAO2_E_GEOMETRY_TYPEINFO)

class KAO2_eTriMesh(KAO2_eGeometry):

    def __init__(self) -> None:

        KAO2_eGeometry.__init__(self)

        self.geo = None

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_TRIMESH_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        KAO2_eGeometry.serialize(self, ar)

        test = [1]
        ar.file.parseInt32(test)
        if 1 != test[0]:
            raise Exception("[KAO2] eTriMesh::serialize():\n\t" + "non-empty member is not supported!")

        self._serializeRefObject(ar, "geo", KAO2_E_GEOSET_TYPEINFO)

    def toBlenderObject(self) -> bpy.types.Object:

        if self.blenderObj is not None:
            return self.blenderObj

        if Settings.blenderObjData is not None:
            raise Exception("[KAO2] eTriMesh::toBlenderObject():\n\t" + "NOT SUPPORTED SETTING!")
        mesh = bpy.data.meshes.new(name = self.name.text)

        Settings.blenderObjData = mesh
        obj = KAO2_eGeometry.toBlenderObject(self)
        Settings.blenderObjData = None

        if self.geo is not None:
            self.geo.updateBlenderMeshObject(mesh, self.name.text)

        if self.material is not None:
            mesh.materials.append(self.material.toBlenderObject())

        return obj

    def rigToBlenderArmature(self, armature_parent: bpy.types.Object, bone_name: str) -> None:

        _debug_header = "[KAO2] eTriMesh::rigToBlenderArmature():\n\t"

        obj = self.blenderObj
        if obj is None:
            raise Exception(_debug_header + "Blender object is missing!")

        if armature_parent is None:
            raise Exception(_debug_header + "Armature parent is missing!")

        parented_to_armature = False
        if obj.parent is None:
            obj.parent = armature_parent
            parented_to_armature = True

        if (self.geo is not None) and (self.geo.phy is not None):

            modifier = obj.modifiers.new(name = "", type = "ARMATURE")
            modifier.object = armature_parent

            self.geo.phy.rigToBlenderArmature(None, bone_name)

            if Settings.ignoreRestPoseUseShapeKeys:
                Settings.armatureModifiedMeshes.append(obj)

        elif parented_to_armature:

            if not bone_name:
                raise Exception(_debug_header + "Bone name is missing!")

            # Workaround for `bpy.ops.pose.armature_apply()`
            # (recalculating object's local transformation)
            bpy.context.collection.objects.link(obj)

            obj.parent_type = "BONE"
            obj.parent_bone = bone_name


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_TRIMESH_TYPEINFO = KAO2_TypeInfo (
    0x3005,
    "eTriMesh",
    KAO2_E_GEOMETRY_TYPEINFO,
    lambda: KAO2_eTriMesh()
)

from .eGeoSet import KAO2_E_GEOSET_TYPEINFO
from .eTransform import KAO2_E_TRANSFORM_TYPEINFO


################################################################
