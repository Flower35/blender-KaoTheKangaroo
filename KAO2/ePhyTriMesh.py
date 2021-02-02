################################################################
# "KAO2/ePhyTriMesh.py"

import bpy

from .Basic import (KAO2_ePoint4, KAO2_eMatrix4x4, KAO2_ePhyVertex)
from .eObject import KAO2_eObject
from .eRefCounter import (KAO2_eRefCounter, KAO2_E_REFCOUNTER_TYPEINFO)

class KAO2_ePhyBone(KAO2_eObject):

    def __init__(self) -> None:

        self.xform = None
        self.matrix = KAO2_eMatrix4x4()

    def serialize(self, ar: "KAO2_Archive") -> None:

        self._serializeRefObject(ar, "xform", KAO2_E_TRANSFORM_TYPEINFO)

        self.matrix.serialize(ar)

        if ar.isInReadMode:

            self.xform.markAsJoint(self.matrix)

            parentLimit = 2
            test = self.xform.parent
            while (parentLimit > 0) and (test is not None):
                test.jointCandidate = True
                test = test.parent
                parentLimit -= 1


class KAO2_ePhyTriMesh(KAO2_eRefCounter):

    def __init__(self):

        self.tri = None
        self.geo = None
        self.vertices = None
        self.bones = []
        self.referenceVertices = [None, None]

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_PHYTRIMESH_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        _debug_header = "[KAO2] ePhyTriMesh::serialize():\n\t"

        self._serializeRefObject(ar, "vertices", KAO2_E_GEOARRAY_PHYVERTEX_TYPEINFO)

        self._serializeSerializables(ar, "bones", KAO2_ePhyBone, None, True)

        from .eGeoSet import KAO2_E_GEOSET_TYPEINFO
        from .eTriMesh import KAO2_E_TRIMESH_TYPEINFO

        self._serializeRefObject(ar, "geo", KAO2_E_GEOSET_TYPEINFO)
        self._serializeRefObject(ar, "tri", KAO2_E_TRIMESH_TYPEINFO)

        if ar.isInReadMode:

            if self.tri is None:
                raise Exception(_debug_header + "\"eTriMesh\" link cannot be empty!")

            node = self.tri
            reason = "mesh \"{}\" has no parent"
            armature = False

            while not armature:
                node = node.parent
                if node is None:
                    reason = reason.format(self.tri.name.text)
                    raise Exception(_debug_header + "Could not guess the Armature parent node - " + reason)
                elif KAO2_eGroup.GROUP_SPECIAL_TYPE_JOINT != node.groupType:
                    node.groupType = KAO2_eGroup.GROUP_SPECIAL_TYPE_ARMATURE
                    print("[KAO2] [DEBUG] Marking node \"{}\" [{}] as ARMATURE PARENT.".format(node.name.text, node.getType().name))
                    armature = True
                else:
                    reason = "all of the \"{}\" mesh parents are bones"

        KAO2_eGeoArray.serialize_3fXArray(ar, self.referenceVertices, 0)
        KAO2_eGeoArray.serialize_3fXArray(ar, self.referenceVertices, 1)

        test = [1]
        ar.file.parseUInt32(test)
        if 1 != test[0]:
            raise Exception("[KAO2] ePhyTriMesh::serialize():\n\t" + "non-empty \"eMorpherMod\" is not supported!")

    def rigToBlenderArmature(self, armature_parent: bpy.types.Object, bone_name: str) -> None:

        _debug_header = "[KAO2] ePhyTriMesh::rigToBlenderArmature():\n\t"

        if (self.tri is None) or (self.tri.blenderObj is None):
            raise Exception(_debug_header + "Blender object is missing!")

        print("-" * 64)
        print(_debug_header[:-2] + " \"{}\"".format(self.tri.name.text))

        obj = self.tri.blenderObj

        # Note: "eTriMesh" is usually linked to the first bone,
        # so we are ignoring the "bone_name".

        # This should corectly position the mesh (relative to
        # parent Armature) in most cases...
        obj.matrix_local = obj.parent.matrix_local.inverted()

        v_groups = []
        for phy_bone in self.bones:
            if phy_bone.xform is None:
                raise Exception(_debug_header + "Bone reference is missing!")
            elif not phy_bone.xform.boneName:
                raise Exception(_debug_header + "Bone name is missing! (xform: \"{}\")".format(phy_bone.xform.name.text))

            v_groups.append(obj.vertex_groups.new(name = phy_bone.xform.boneName))

        if self.vertices is None:
            raise Exception(_debug_header + "Bone indices and weights are missing!")

        v_count = len(obj.data.vertices)
        if (len(self.vertices.data) != v_count) or (len(self.referenceVertices[1].data) != v_count) or (len(self.referenceVertices[0].data) != v_count):
            raise Exception(_debug_header + "vertex lists size mismatch!")

        for i in range (0, v_count):

            vert = self.referenceVertices[1].data[i]
            norm = self.referenceVertices[0].data[i]

            obj.data.vertices[i].co = [vert.x, vert.y, vert.z]
            obj.data.vertices[i].normal = [norm.x, norm.y, norm.z]

            phy_vert = self.vertices.data[i]

            j = 0
            while j < 3:
                bone_idx = phy_vert.index[j]
                if 0x80 == (0x80 & bone_idx):
                    j = 3
                else:
                    if (bone_idx < 0) or (bone_idx >= len(self.bones)):
                        raise Exception(_debug_header + "bone index out of range!")

                    w = phy_vert.weight[j]
                    if (w < 0) or (w > 1.0):
                        if (w > -1e-6) and (w <= 0):
                            w = 0
                        else:
                            raise Exception(_debug_header + "invalid bone weight! ({})".format(w))

                    v_groups[bone_idx].add(index = [i], weight = w, type = "ADD")
                    j += 1


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_PHYTRIMESH_TYPEINFO = KAO2_TypeInfo (
    0x3003,
    "ePhyTriMesh",
    KAO2_E_REFCOUNTER_TYPEINFO,
    lambda: KAO2_ePhyTriMesh()
)

from .eGroup import KAO2_eGroup
from .eTransform import KAO2_E_TRANSFORM_TYPEINFO
from .eGeoArray import (KAO2_eGeoArray, KAO2_E_GEOARRAY_PHYVERTEX_TYPEINFO)


################################################################
