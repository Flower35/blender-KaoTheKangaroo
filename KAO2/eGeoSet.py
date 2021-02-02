################################################################
# "KAO2/eGeoSet.py"

import bpy

from .eRefCounter import (KAO2_eRefCounter, KAO2_E_REFCOUNTER_TYPEINFO)

class KAO2_eGeoSet(KAO2_eRefCounter):

    def __init__(self) -> None:

        self.unknown_08 = 0
        self.defaultVertexCount = 0
        self.texCoordsCount = 1
        self.stripsArray = None
        self.indicesArray = None
        self.verticesArray = [None, None]
        self.normalsArray = [None, None]
        self.texCoordsArray = [None, None, None, None]
        self.colorsArray = None
        self.texCoordsId = [0, 0, 0, 0]
        self.currentSet = 0
        self.phy = None
        self.aabbTree = None

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_GEOSET_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        self._serializeUInt32(ar, "unknown_08")
        self._serializeUInt32(ar, "defaultVertexCount")

        self._serializeRefObject(ar, "indicesArray", KAO2_E_GEOARRAY_USHORT_TYPEINFO)

        KAO2_eGeoArray.serialize_3fXArray(ar, self.verticesArray, 0)
        KAO2_eGeoArray.serialize_3fXArray(ar, self.normalsArray, 0)

        self._serializeUInt32(ar, "texCoordsCount")
        if (self.texCoordsCount < 0) or (self.texCoordsCount > 4):
            raise Exception("[KAO2] eGeoSet::serialize():\n\t" + "Invalid number of tex coord arrays!")

        for i in range (0, self.texCoordsCount):
            ar.serialize(self.texCoordsArray, i, KAO2_E_GEOARRAY_POINT2_TYPEINFO)
            ar.file.parseUInt32(self.texCoordsId, i)

        if ar.isInReadMode:
            for i in range (self.texCoordsCount, 4):
                self.texCoordsArray[i] = None
                self.texCoordsId[i] = 0

        self._serializeRefObject(ar, "colorsArray", KAO2_E_GEOARRAY_POINT4_TYPEINFO)

        self._serializeRefObject(ar, "stripsArray", KAO2_E_GEOARRAY_USHORT_TYPEINFO)

        self._serializeRefObject(ar, "aabbTree", KAO2_E_GEOARRAY_ABB_TYPEINFO)

        self._serializeRefObject(ar, "phy", KAO2_E_PHYTRIMESH_TYPEINFO)

    def updateBlenderMeshObject(self, mesh: bpy.types.Mesh, name: str) -> None:

        _debug_header = "[KAO2] eGeoSet::updateBlenderMeshObject():\n\t"

        print("-" * 64)
        print(_debug_header[:-2] + " \"{}\"".format(name))

        if self.verticesArray[0] is None:
            raise Exception(_debug_header + "no vertices!")

        verts = self.verticesArray[0].data
        v_count = len(verts)

        ################################

        print(_debug_header + "Generating loops and polygons...")

        mesh_faces = []

        if self.stripsArray is not None:

            strips = self.stripsArray.data

            indices = None if (self.indicesArray is None) else self.indicesArray.data

            idx_total = 0
            for ts in strips:

                if ts.x < 3:
                    raise Exception(_debug_header + "Less than three indices for \"TRIANGLE_STRIP\" entry!")

                face = []

                # WORKAROUND: changing TRIANGLE STRIPS to regular TRIANGLES
                for a in range (0, ts.x - 2):
                    b = a % 2
                    face = []
                    for c in (0, 1 + b, 2 - b):
                        d = idx_total + a + c
                        face.append(d if (indices is None) else indices[d].x)
                    mesh_faces.append(face)

                #@@ idx =  ts.x % 2
                #@@ limit_a = idx_total + ts.x - 1 - idx
                #@@ limit_b = idx_total + ts.x - 2 + idx

                #@@ face.append(idx_total if (indices is None) else indices[idx_total].x)

                #@@ idx = idx_total + 1
                #@@ while idx <= limit_a:
                #@@     face.append(idx if (indices is None) else indices[idx].x)
                #@@     idx += 2

                #@@ idx = limit_b
                #@@ while idx >= (idx_total + 2):
                #@@     face.append(idx if (indices is None) else indices[idx].x)
                #@@     idx -= 2

                #@@ mesh_faces.append(face)
                idx_total += ts.x

        else:

            indices = None if (self.indicesArray is None) else self.indicesArray.data

            idx_count = v_count if (indices is None) else len(indices)

            if (indices is not None) and (0 != (len(indices) % 3)):
                raise Exception(_debug_header + "\"TRIANGLE\" indices size not divisible by 3!")
            elif 0 != (v_count % 3):
                raise Exception(_debug_header + "vertex count not divisible by 3!")

            idx = 0
            while idx < idx_count:
                face = []
                for i in range(0, 3):
                    j = idx + i
                    face.append(j if (indices is None) else indices[j].x)
                mesh_faces.append(face)
                idx += 3

        loops_vert_idx = []
        faces_loop_start = []
        faces_loop_total = []

        loop_idx = 0
        for face in mesh_faces:
            for i in face:
                if (i < 0) or (i >= v_count):
                    raise Exception(_debug_header + "vertex index ouf of range!")
            idx_count = len(face)
            loops_vert_idx.extend(face)
            faces_loop_start.append(loop_idx)
            faces_loop_total.append(idx_count)
            loop_idx += idx_count

        mesh.loops.add(len(loops_vert_idx))
        mesh.polygons.add(len(mesh_faces))

        mesh.loops.foreach_set("vertex_index", loops_vert_idx)
        mesh.polygons.foreach_set("loop_start", faces_loop_start)
        mesh.polygons.foreach_set("loop_total", faces_loop_total)

        ################################

        print(_debug_header + "Updating vertices...")

        normals = None
        if self.normalsArray[0] is not None:
            normals = self.normalsArray[0].data

            if v_count != len(normals):
                raise Exception(_debug_header + "vertices and normals size mismatch!")

        mesh.vertices.add(v_count)

        for i in range (0, v_count):
            mesh.vertices[i].co = [verts[i].x, verts[i].y, verts[i].z]
            if normals is not None:
                mesh.vertices[i].normal = [normals[i].x, normals[i].y, normals[i].z]

        ################################

        uv = None
        if self.texCoordsArray[0] is not None:

            uv = self.texCoordsArray[0].data

            if v_count != len(uv):
                raise Exception(_debug_header + "vertices and UVs size mismatch!")

            uv_layer = mesh.uv_layers.new(do_init = False)
            if len(mesh.loops) != len(uv_layer.data):
                raise Exception(_debug_header + "loops and generated UVs size mismatch!")

        colors = None
        if self.colorsArray is not None:

            colors = self.colorsArray.data

            if v_count != len(colors):
                raise Exception(_debug_header + "vertices and colors size mismatch!")

            vcol_layer = mesh.vertex_colors.new(do_init = False)
            if len(mesh.loops) != len(vcol_layer.data):
                raise Exception(_debug_header + "loops and generated colors size mismatch!")

        if (uv is not None) or (colors is not None):
            for loop_idx, loop in enumerate(mesh.loops):
                i = loop.vertex_index
                if uv is not None:
                    uv_layer.data[loop_idx].uv = [uv[i].x, 1.0 - uv[i].y]
                if colors is not None:
                    vcol_layer.data[loop_idx].color = [colors[i].x, colors[i].y, colors[i].z, colors[i].w]

        ################################

        mesh.validate(clean_customdata = False)
        mesh.update(calc_edges = False)


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_GEOSET_TYPEINFO = KAO2_TypeInfo (
    0x3004,
    "eGeoSet",
    KAO2_E_REFCOUNTER_TYPEINFO,
    lambda: KAO2_eGeoSet()
)

from .eGeoArray import (KAO2_eGeoArray, KAO2_E_GEOARRAY_USHORT_TYPEINFO, KAO2_E_GEOARRAY_POINT2_TYPEINFO, KAO2_E_GEOARRAY_POINT4_TYPEINFO, KAO2_E_GEOARRAY_ABB_TYPEINFO)
from .ePhyTriMesh import KAO2_E_PHYTRIMESH_TYPEINFO


################################################################
