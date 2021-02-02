################################################################
# "KAO2/eBitmap.py"

import bpy
import os
import traceback

from ..KaoUtility import *

from .eRefCounter import (KAO2_eRefCounter, KAO2_E_REFCOUNTER_TYPEINFO)

class KAO2_eBitmap(KAO2_eRefCounter):

    BITMAP_TYPE_RGBA8 = 0
    BITMAP_TYPE_RGB8 = 1
    BITMAP_TYPE_PAL8_RGBA8 = 2
    BITMAP_TYPE_PAL8_RGBX8 = 3
    BITMAP_TYPE_RGBX8 = 4

    BITMAP_LOADED_RAW = 0
    BITMAP_LOADED_QUEUED = 1
    BITMAP_LOADED_OK = 2

    def __init__(self) -> None:

        self.virtualWidth = 0
        self.virtualHeight = 0
        self.width = 0
        self.height = 0
        self.pixels = None
        self.palette = None
        self.bitmapType = KAO2_eBitmap.BITMAP_TYPE_RGBA8
        self.path = KAO2_eString()

        self.isLoaded = KAO2_eBitmap.BITMAP_LOADED_RAW
        self.blenderObj = None

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_BITMAP_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        can_be_empty = (ar.version >= 0x8A) and (KAO2_eBitmap.BITMAP_LOADED_OK == self.isLoaded)

        if (not ar.isInReadMode) and can_be_empty:

            for i in range (0, 2):
                ar.file.parseUInt32([0])

        else:

            self._serializeUInt32(ar, "virtualWidth")
            self._serializeUInt32(ar, "virtualHeight")

        if (not ar.isInReadMode) and can_be_empty:

            for i in range (0, 2):
                ar.file.parseUInt32([0])

        else:

            self._serializeUInt32(ar, "width")
            self._serializeUInt32(ar, "height")

            if (not self.__validateWidth(self.width)) or (not self.__validateWidth(self.height)):
                raise Exception("[KAO2] eBitmap::serialize():\n\t" + "Incorrect image dimensions! (should be a power of 2, between 0 and 2048).")

        self._serializeUInt32(ar, "bitmapType")

        if (self.bitmapType < 0) or (self.bitmapType > 4):
            raise Exception("[KAO2] eBitmap::serialize():\n\t" + "Unsupported image type 0x{08X}!".format(self.bitmapType))

        total_length = self.__getBytesPerPixel() * self.width * self.height

        if (not can_be_empty) and (total_length > 0):
            test = [self.pixels]
            ar.file.parseBytes(test, total_length)
            self.pixels = test[0]

        if self.__isUsingPalette():
            test = [self.palette]
            ar.file.parseBytes(test, 1024)
            self.palette = test[0]
        else:
            self.palette = None

        self._serializeString(ar, "path")

        if ar.isInReadMode and ((self.virtualWidth <= 0) or (self.virtualHeight <= 0)):
            self.isLoaded = KAO2_eBitmap.BITMAP_LOADED_QUEUED

        test = [1]
        ar.file.parseInt32(test)
        if 1 != test[0]:
            raise Exception("[KAO2] eBitmap::serialize():\n\t" + "non-empty member is not supported!")

    @staticmethod
    def __validateWidth(value: int) -> bool:

        if (value < 0) or (value > 2048):
            return False

        if value <= 2:
            return True

        return not (value & (value - 1))

    def __getBytesPerPixel(self) -> int:

        test = {
            KAO2_eBitmap.BITMAP_TYPE_RGBA8: 4,
            KAO2_eBitmap.BITMAP_TYPE_RGB8: 3,
            KAO2_eBitmap.BITMAP_TYPE_PAL8_RGBA8: 1,
            KAO2_eBitmap.BITMAP_TYPE_PAL8_RGBX8: 1,
            KAO2_eBitmap.BITMAP_TYPE_RGBX8: 4
        }

        return test.get(self.bitmapType, 0)

    def __isUsingPalette(self) -> bool:

        return self.bitmapType in (
            KAO2_eBitmap.BITMAP_TYPE_PAL8_RGBA8,
            KAO2_eBitmap.BITMAP_TYPE_PAL8_RGBX8 )

    def __hasAlphaChanel(self) -> bool:

        return self.bitmapType in (
            KAO2_eBitmap.BITMAP_TYPE_RGBA8,
            KAO2_eBitmap.BITMAP_TYPE_PAL8_RGBA8 )

    def toBlenderObject(self) -> bpy.types.Image:

        _debug_header = "[KAO2] eBitmap::toBlenderObject():\n\t"

        if self.blenderObj is not None:
            return self.blenderObj

        elif KAO2_eBitmap.BITMAP_LOADED_QUEUED == self.isLoaded:

            path = os.path.join(Settings.workspaceDir, self.path.text)

            print(_debug_header + "Loading \"{}\"".format(path))

            try:
                image = bpy.data.images.load(filepath = path)
            except RuntimeError:
                image = None
                traceback.print_exc(limit = 1)

        elif KAO2_eBitmap.BITMAP_LOADED_RAW == self.isLoaded:

            image = bpy.data.images.new(name = self.path.text, width = self.width, height = self.height, alpha = self.__hasAlphaChanel())

            total_length = 4 * self.width * self.height
            assert len(image.pixels) == total_length, _debug_header + "Pixels length mismatch!"

            print(_debug_header + "Converting RAW pixels (\"{}\"), please wait... (THIS CAN TAKE A FEW MINUTES!)".format(self.path.text))

            d_offs = total_length - 4 * self.width
            s_offs = 0

            if self.bitmapType in (KAO2_eBitmap.BITMAP_TYPE_RGBA8, KAO2_eBitmap.BITMAP_TYPE_RGBX8):

                for y in range(0, self.height):

                    for x in range(0, self.width):

                        for p in range (0, 4):

                            image.pixels[d_offs] = self.pixels[s_offs] / 255.0
                            d_offs += 1
                            s_offs += 1

                    d_offs -= 8 * self.width

            elif KAO2_eBitmap.BITMAP_TYPE_RGB8 == self.bitmapType:

                for y in range(0, self.height):

                    for x in range(0, self.width):

                        for p in range (0, 3):

                            image.pixels[d_offs] = self.pixels[s_offs] / 255.0
                            d_offs += 1
                            s_offs += 1

                        image.pixels[d_offs] = 1.0
                        d_offs += 1

                    d_offs -= 8 * self.width

            elif self.bitmapType in (KAO2_eBitmap.BITMAP_TYPE_PAL8_RGBA8, KAO2_eBitmap.BITMAP_TYPE_PAL8_RGBX8):

                assert (self.palette is not None) and (1024 == len(self.palette)), "[KAO2] eBitmap::toBlenderObject():\n\t" + "Missing color palette!"

                for y in range(0, self.height):

                    for x in range(0, self.width):

                        index = 4 * self.pixels[s_offs]
                        s_offs += 1

                        for p in range(0, 4):

                            image.pixels[d_offs] = self.palette[index] / 255.0
                            index += 1
                            d_offs += 1

                    d_offs -= 8 * self.width

            else:
                raise Exception("[KAO2] eBitmap::toBlenderObject():\n\t" + "Unsupported image type 0x{08X}!".format(self.bitmapType))

        else:
            return None

        print(_debug_header + "RAW conversion done!")
        self.isLoaded = KAO2_eBitmap.BITMAP_LOADED_OK
        self.blenderObj = image
        return image

    def fromBlenderObject(self, image: bpy.types.Image) -> None:

        if (self.blenderObj is not None) or (KAO2_eBitmap.BITMAP_LOADED_OK == self.isLoaded):
            raise Exception("[KAO2] eBitmap::fromBlenderObject():\n\t" + "bitmap already created...")

        total_length = 4 * self.width * self.height
        assert len(image.pixels) == total_length, "[KAO2] eBitmap::fromBlenderObject():\n\t" + "Pixels length mismatch!"

        assert 4 == image.channels, "[KAO2] eBitmap::fromBlenderObject():\n\t" + "Color channels mismatch!"
        self.bitmapType = KAO2_eBitmap.BITMAP_TYPE_RGBA8
        self.pixels = bytearray(total_length)
        self.palette = []

        d_offs = total_length - 4 * self.width
        s_offs = 0

        for y in range(0, self.height):

            for x in range(0, self.width):

                for p in range (0, 4):

                    self.pixels[d_offs] = round(image.pixels[s_offs] * 255.0)
                    d_offs += 1
                    s_offs += 1

            d_offs -= 8 * self.width

        try:
            self.path = KAO2_eString(os.path.relpath(path = image.filepath, start = Settings.workspaceDir))
        except ValueError:
            self.path = KAO2_eString("")

        self.isLoaded = KAO2_eBitmap.BITMAP_LOADED_OK
        self.blenderObj = image


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_BITMAP_TYPEINFO = KAO2_TypeInfo (
    0x1001,
    "eBitmap",
    KAO2_E_REFCOUNTER_TYPEINFO,
    lambda: KAO2_eBitmap()
)

from .eString import KAO2_eString


################################################################
