################################################################
# "KAO2/eTexture.py"

import bpy
from mathutils import Vector, Quaternion

from .eRefCounter import (KAO2_eRefCounter, KAO2_E_REFCOUNTER_TYPEINFO)

class KAO2_eTexture(KAO2_eRefCounter):

    def __init__(self) -> None:

        self.textureFlags = 0x04
        self.transform = None
        self.bmp = None
        self.unknown_14 = 0

        self.blenderObj = None

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_TEXTURE_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        self._serializeRefObject(ar, "bmp", KAO2_E_BITMAP_TYPEINFO)

        self._serializeUInt32(ar, "textureFlags")

        self._serializeRefObject(ar, "transform", KAO2_E_TEXTRANSFORM_TYPEINFO)

        self._serializeUInt32(ar, "unknown_14")



    def toBlenderObject(self) -> bpy.types.ImageTexture:

        if self.blenderObj is not None:
            return self.blenderObj

        tex = bpy.data.textures.new(name = "", type = "IMAGE")

        if self.bmp is not None:
            tex.image = self.bmp.toBlenderObject()

        # TODO: animated textures

        self.blenderObj = tex
        return tex

    def fromBlenderObject(self, tex: bpy.types.ImageTexture) -> None:

        if self.blenderObj is not None:
            if self.blenderObj is not tex:
                raise Exception("[KAO2] eTexture::fromBlenderObject():\n\t" + "texture already created...")
            else:
                return

        # TODO: jak przypisać "KAO2_eBitmap" do "bpy.types.ImageTexture"

        self.blenderObj = tex


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_TEXTURE_TYPEINFO = KAO2_TypeInfo (
    0x1002,
    "eTexture",
    KAO2_E_REFCOUNTER_TYPEINFO,
    lambda: KAO2_eTexture()
)

from .eBitmap import KAO2_E_BITMAP_TYPEINFO
from .eTexTransform import KAO2_E_TEXTRANSFORM_TYPEINFO


################################################################
