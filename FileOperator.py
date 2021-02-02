
################################################################
# "FileOperator.py"

import struct
from typing import List


class FileOperator(object):

    def __init__(self, path: str, read_or_write: bool) -> None:

        self.__file = open(path, "rb" if read_or_write else "wb")
        self.__isInReadMode = read_or_write

    def jumpToOffset(self, offset: int) -> None:

        self.__file.seek(offset)

    def __parseData(self, arg: List, index: int, format: str, length: int) -> None:

        if self.__isInReadMode:

            test = self.__file.read(length)
            test = struct.unpack("<" + format, test)[0]

            if len(arg) > index:
                arg[index] = test

            elif len(arg) == index:
                arg.append(test)

            else:
                raise Exception("[KAO] FileOperator::__parseData():\n\t" + "array index out of bounds!")

        else:

            test = struct.pack("<" + format, arg[index])

            if len(test) != length:
                raise Exception("[KAO] FileOperator::__parseData():\n\t" + "Size mismatch.")

            self.__file.write(test)

    def parseInt32(self, arg: List[int], index: int = 0) -> None:

        self.__parseData(arg, index, "i", 4)

    def parseUInt32(self, arg: List[int], index: int = 0) -> None:

        self.__parseData(arg, index, "I", 4)

    def parseInt16(self, arg: List[int], index: int = 0) -> None:

        self.__parseData(arg, index, "h", 2)

    def parseUInt16(self, arg: List[int], index: int = 0) -> None:

        self.__parseData(arg, index, "H", 2)

    def parseInt8(self, arg: List[int], index: int = 0) -> None:

        self.__parseData(arg, index, "b", 1)

    def parseUInt8(self, arg: List[int], index: int = 0) -> None:

        self.__parseData(arg, index, "B", 1)

    def parseFloat(self, arg: List[float], index: int = 0) -> None:

        self.__parseData(arg, index, "f", 4)

    def parseBytes(self, arg: List[bytes], length) -> None:

        if self.__isInReadMode:

            test = self.__file.read(length)

            if len(arg) > 0:

                arg[0] = test

            else:

                arg.append(test)

        else:

            if len(arg[0]) != length:
                raise Exception("[KAO] FileOperator::parseBytes():\n\t" + "Size mismatch.")

            self.__file.write(arg[0])


################################################################
