################################################################
# "KAO2/Archive.py"

from typing import (Any, List)

class KAO2_Archive(object):

    ARCHIVE_MAGIC = 0x65746174 # "tate"
    ARCHIVE_ITEM_OBJECT = 0
    ARCHIVE_ITEM_STRING = 1
    ARCHIVE_ITEM_OTHER = 2

    def __init__(self) -> None:

        self.__parent = None

    def open(self, path: str, read_or_write: bool, game_version: str) -> None:

        _debug_header = "[KAO2] Archive::open():\n\t"
        print("-" * 64)
        print(_debug_header[:-2] + " \"{}\"".format(path))

        self.__path = path
        self.isInReadMode = read_or_write
        self.__gameVersion = game_version

        self.file = FileOperator(self.__path, self.isInReadMode)

        if "KAO2_PL" == self.__gameVersion:
            ar_version_min = 0x82
            ar_version_max = 0x87
        elif "KAO2_USA" == self.__gameVersion:
            ar_version_min = 0x82
            ar_version_max = 0x89
        elif "KAO_TW" == self.__gameVersion:
            ar_version_min = 0x8B
            ar_version_max = 0x90
        else:
            raise Exception(_debug_header + "Unrecognized game version.")

        # Check archive magic and archive version

        test = [KAO2_Archive.ARCHIVE_MAGIC]
        self.file.parseUInt32(test)

        if (self.isInReadMode) and (KAO2_Archive.ARCHIVE_MAGIC != test[0]):
            raise Exception(_debug_header + "Invalid archive magic. Expected \"tate\".")

        test = [ar_version_max]
        self.file.parseUInt32(test)
        self.version = test[0]

        if (self.isInReadMode) and ((self.version < ar_version_min) or (self.version > ar_version_max)):
            raise Exception(_debug_header + "Invalid archive version {}.\n\t".format(self.version) + "(current version: {}, minimum: {}).".format(ar_version_max, ar_version_min))

        # Get the number of temporary items

        test = [65536]
        self.file.parseUInt32(test)
        self.__itemsMaxLength = test[0]
        self.__items = []

        # Begin serialization

        from .eRefCounter import KAO2_E_REFCOUNTER_TYPEINFO

        test = [self.__parent]
        self.serialize(test, 0, KAO2_E_REFCOUNTER_TYPEINFO)
        self.__parent = test[0]

        # Finish serialization

        del self.__items[:]

        if not self.isInReadMode:
            self.file.jumpToOffset(0x08)
            test = [len(self.__items)]
            self.file.parseUInt32(test)

    def addItem(self, obj: Any, obj_type: int) -> None:

        if len(self.__items) >= self.__itemsMaxLength:
            raise Exception("[KAO2] Archive::addItem():\n\t" + "Archive initialized incorrectly?\n\t" + "Not enough space for temporary classes! (current size: {}).".format(self.__itemsMaxLength))

        self.__items.append([obj, obj_type])

    def getItem(self, index: int, obj_type: int) -> Any:

        if (index < 0) or (index >= len(self.__items)):
            raise Exception("[KAO2] Archive::getItem():\n\t" + "Incorrect temporary item Index... ({}/{})\n\t".format(index, len(self.__items)) + "THIS SHOULD NEVER HAPPEN !!!")

        if self.__items[index][1] != obj_type:
            raise Exception("[KAO2] Archive::getItem():\n\t" + "Incorrect temporary item Type...\n\t" + "THIS SHOULD NEVER HAPPEN !!!")

        return self.__items[index][0]


    def findItem(self, obj) -> int:

        for index, item in enumerate(self.__items):

            if item[0] is obj:

                return index

        return (-1)

    @staticmethod
    def serializationTypesCheck(current_info: "KAO2_TypeInfo", info: "KAO2_TypeInfo") -> None:

        if (info is not None) and not current_info.checkHierarchy(info):
            raise Exception("[KAO2] Archive::serialize():\n\t" + "Wrong object type in archive!\n\t" + "Expected: 0x{:08X} [{}]\n\t".format(info.index, info.name) + "Current TypeInfo: 0x{:08X} [{}]".format(current_info.index, current_info.name))

    def serialize(self, obj: List["KAO2_eObject"], index: int, info: "KAO2_TypeInfo") -> None:

        if self.isInReadMode:

            test = []
            self.file.parseUInt32(test)

            if 0 == test[0]:

                self.file.parseUInt32(test)

                new_info = KAO2_TypeInfo.getTypeInfo(test[0])

                KAO2_Archive.serializationTypesCheck(new_info, info)

                obj[index] = new_info.create()

                if obj[index] is None:
                    raise Exception("[KAO2] Archive::serialize():\n\t" + "Abstract object deserialization!\n\t" + "Current TypeInfo: 0x{:08X} [{}]".format(new_info.index, new_info.name))

                self.addItem(obj[index], KAO2_Archive.ARCHIVE_ITEM_OBJECT)

                obj[index].serialize(self)

            elif 1 == test[0]:

                obj[index] = None

            else:

                obj[index] = self.getItem(test[0] - 2, KAO2_Archive.ARCHIVE_ITEM_OBJECT)

                new_info = obj[index].getType()

                KAO2_Archive.serializationTypesCheck(new_info, info)

        else:

            if obj[index] is not None:

                test = self.findItem(obj[index])

                if test < 0:

                    self.addItem(obj[index], KAO2_Archive.ARCHIVE_ITEM_OBJECT)

                    self.file.parseUInt32([0])
                    self.file.parseUInt32([obj[index].getType().index])

                    obj[index].serialize(self)

                else:

                    self.file.parseUInt32([test + 2])

            else:

                self.file.parseUInt32([1])

    def __findAndReplaceExactString(self, obj: List["KAO2_eString"]) -> None:

        # The built-in comparison function works well with empty strings

        for item in self.__items:
            if (KAO2_Archive.ARCHIVE_ITEM_STRING == item[1]) and (item[0].text == obj[0].text):
                obj[0] = item[0]
                return

    def serializeString(self, obj: List["KAO2_eString"]) -> None:

        if self.isInReadMode:

            test = []
            self.file.parseUInt32(test)

            if 0 == test[0]:

                obj[0] = KAO2_eString()
                obj[0].readString(self)

                self.addItem(obj[0], KAO2_Archive.ARCHIVE_ITEM_STRING)

            elif 1 == test[0]:

                obj[0] = None

            else:

                obj[0] = self.getItem(test[0] - 2, KAO2_Archive.ARCHIVE_ITEM_STRING)

        else:

            if obj[0] is not None:

                self.__findAndReplaceExactString(obj)

                test = self.findItem(obj[0])

                if test < 0:

                    self.addItem(obj[0], KAO2_Archive.ARCHIVE_ITEM_STRING)

                    self.file.parseUInt32([0])

                    obj[0].writeString(self)

                else:

                    self.file.parseUInt32([test + 2])

            else:

                raise Exception("[KAO2] Archive::serializeString():\n\t" + "Empty String pointers are not supported by Kao2 engine!")

    def convertToBlender(self, workspace_dir: str, inv_bind_matrices: bool, no_rest_pose: bool, load_anims: bool) -> Any:

        if self.__parent is not None:

            Settings.reset()
            Settings.workspaceDir = workspace_dir
            Settings.ignoreInvBindMatrices = not inv_bind_matrices
            Settings.ignoreRestPoseUseShapeKeys = no_rest_pose

            obj = self.__parent.toBlenderObject()

            if load_anims:
                print("-" * 64)
                print("Parsing animation keyframes... ")

                self.__parent.updateBlenderAnims()

            return obj


################################################################

from ..FileOperator import FileOperator
from ..KaoUtility import *
from .TypeInfo import KAO2_TypeInfo
from .eString import KAO2_eString


################################################################
