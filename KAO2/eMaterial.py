################################################################
# "KAO2/eMaterial.py"

import bpy
from bpy_extras import node_shader_utils

from .eRefCounter import (KAO2_eRefCounter, KAO2_E_REFCOUNTER_TYPEINFO)

class KAO2_eMaterial(KAO2_eRefCounter):

    def __init__(self) -> None:

        self.textures = []
        self.materialFlags = 0x00
        self.state = None
        self.collisionType = 0x0000
        self.unknown_20 = 0x0000
        self.soundType = 0x0000
        self.name = KAO2_eString()
        self.transpLayer = 0
        self.alphaTestRef = 0.5

        self.blenderObj = None

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_MATERIAL_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        self._serializeRefObjectArray(ar, "textures", KAO2_E_TEXTURE_TYPEINFO)

        self._serializeUInt8(ar, "materialFlags")

        self._serializeRefObject(ar, "state", KAO2_E_MATERIALSTATE_TYPEINFO)

        self._serializeUInt32(ar, "collisionType")
        self._serializeUInt16(ar, "unknown_20")
        self._serializeUInt16(ar, "soundType")

        self._serializeString(ar, "name")

        self._serializeUInt32(ar, "transpLayer")
        self._serializeFloat(ar, "alphaTestRef")

    def toBlenderObject(self) -> bpy.types.Material:

        if self.blenderObj is not None:
            return self.blenderObj

        mat = bpy.data.materials.new(name = self.name.text)

        if len(self.textures) >= 1:

            mat_wrap = node_shader_utils.PrincipledBSDFWrapper(mat, is_readonly = False)
            mat_wrap.use_nodes = True

            tex = self.textures[0].toBlenderObject()
            node_tex = mat_wrap.base_color_texture

            node_tex.image = tex.image
            node_tex.texcoords = "UV"

        # TODO: dodać WSZYSTKIE podtesktury

        self.blenderObj = mat
        return mat

    def fromBlenderObject(self, mat: bpy.types.Material) -> None:

        if self.blenderObj is not None:
            raise Exception("[KAO2] eMaterial::fromBlenderObject():\n\t" + "material already created...")

        # TODO: patrz "eTexture.py"

        self.blenderObj = mat


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_MATERIAL_TYPEINFO = KAO2_TypeInfo (
    0x1003,
    "eMaterial",
    KAO2_E_REFCOUNTER_TYPEINFO,
    lambda: KAO2_eMaterial()
)

from .eString import KAO2_eString
from .eTexture import KAO2_E_TEXTURE_TYPEINFO
from .eMaterialState import KAO2_E_MATERIALSTATE_TYPEINFO


################################################################
