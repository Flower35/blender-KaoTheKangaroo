################################################################
# "KAO2/Basic.py"

from math import (sqrt, sin, cos)
from mathutils import Vector, Quaternion, Matrix
from typing import Any, Tuple, List


class KAO2_Serializable(object):

    def serialize(self, ar: "KAO2_Archive") -> None:

        raise Exception("[KAO2] serialize():\n\t" + "METHOD IS NOT OVERRIDDEN!!!")

    def __numberSerializationTemplate(self, ar: "KAO2_Archive", prop_name: str, func_name: str) -> Any:

        test = [getattr(self, prop_name)]
        getattr(ar.file, "parse" + func_name)(test)
        setattr(self, prop_name, test[0])

    def __arraySerializationTemplate(self, ar: "KAO2_Archive", array_name: str, func_name: str, use_length: bool) -> Any:

        array = getattr(self, array_name)
        length = len(array)

        if use_length:

            if ar.isInReadMode:

                del array[:]

                test = []
                ar.file.parseUInt32(test)
                length = test[0]

                array = [None] * length
                setattr(self, array_name, array)

            else:

                ar.file.parseUInt32([length])

        for i in range(0, length):

            getattr(ar.file, "parse" + func_name)(array, i)

    def _serializeUInt32(self, ar: "KAO2_Archive", prop_name: str) -> None:

        self.__numberSerializationTemplate(ar, prop_name, "UInt32")

    def _serializeUInt16(self, ar: "KAO2_Archive", prop_name: str) -> None:

        self.__numberSerializationTemplate(ar, prop_name, "UInt16")

    def _serializeUInt8(self, ar: "KAO2_Archive", prop_name: str) -> None:

        self.__numberSerializationTemplate(ar, prop_name, "UInt8")

    def _serializeFloat(self, ar: "KAO2_Archive", prop_name: str) -> None:

        self.__numberSerializationTemplate(ar, prop_name, "Float")

    def _serializeUInt32Array(self, ar: "KAO2_Archive", array_name: str, use_length: bool) -> None:

        self.__arraySerializationTemplate(ar, array_name, "UInt32", use_length)

    def _serializeUInt8Array(self, ar: "KAO2_Archive", array_name: str, use_length: bool) -> None:

        self.__arraySerializationTemplate(ar, array_name, "UInt8", use_length)

    def _serializeFloatArray(self, ar: "KAO2_Archive", array_name: str, use_length: bool) -> None:

        self.__arraySerializationTemplate(ar, array_name, "Float", use_length)

    def _serializeSerializables(self, ar: "KAO2_Archive", array_name: str, class_type: type, subclass_type: type, use_length: bool) -> None:

        if not issubclass(class_type, KAO2_Serializable):
            raise Exception("[KAO2] _serializeSerializables():\n\t" + "invalid class type!")

        array = getattr(self, array_name)

        if use_length:

            if ar.isInReadMode:

                del array[:]

                test = []
                ar.file.parseUInt32(test)

                for i in range (0, test[0]):
                    array.append(class_type() if subclass_type is None else class_type(subclass_type))
                    array[-1].serialize(ar)

                return

            ar.file.parseUInt32([len(array)])

        elif ar.isInReadMode:

            for i in range(0, len(array)):
                array[i] = class_type() if subclass_type is None else class_type(subclass_type)
                array[i].serialize(ar)

            return

        for obj in array:

            if (not isinstance(obj, class_type)) or ((subclass_type is not None) and (subclass_type is not obj._subclass_type)):
                raise Exception("[KAO2] _serializeSerializables():\n\t" + "invalid object type!")

            obj.serialize(ar)

    def _serializeString(self, ar: "KAO2_Archive", prop_name: str) -> None:

        test = [getattr(self, prop_name)]
        ar.serializeString(test)
        setattr(self, prop_name, test[0])


class KAO2_eUInt16(KAO2_Serializable):

    def __init__(self, x: int = 0) -> None:

        self.x = x

    def serialize(self, ar: "KAO2_Archive") -> None:

        self._serializeUInt16(ar, "x")


class KAO2_ePoint1(KAO2_Serializable):

    def __init__(self, x: float = 1.0) -> None:

        self.x = x

    def serialize(self, ar: "KAO2_Archive") -> None:

        self._serializeFloat(ar, "x")


class KAO2_ePoint2(KAO2_Serializable):

    def __init__(self, x: float = 0, y: float = 0) -> None:

        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:

        if isinstance(other, KAO2_ePoint2):
            return \
                (self.x == other.x) and \
                (self.y == other.y)

        return False

    def __add__(self, other) -> "KAO2_ePoint2":

        if isinstance(other, KAO2_ePoint2):
            return KAO2_ePoint2 (
                self.x + other.x,
                self.y + other.y )

        return None

    def __mul__(self, scalar) -> "KAO2_ePoint2":

        if isinstance(scalar, (int, float)):
            return KAO2_ePoint2 (
                self.x * scalar,
                self.y * scalar )

        return None

    def serialize(self, ar: "KAO2_Archive") -> None:

        self._serializeFloat(ar, "x")
        self._serializeFloat(ar, "y")

class KAO2_ePoint3(KAO2_Serializable):

    def __init__(self, x: float = 0, y: float = 0, z: float = 0) -> None:

        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other) -> bool:

        if isinstance(other, KAO2_ePoint3):
            return \
                (self.x == other.x) and \
                (self.y == other.y) and \
                (self.z == other.z)

        return False

    def __add__(self, other) -> "KAO2_ePoint3":

        if isinstance(other, KAO2_ePoint3):
            return KAO2_ePoint3 (
                self.x + other.x,
                self.y + other.y,
                self.z + other.z )

        return None

    def __sub__(self, other) -> "KAO2_ePoint3":

        if isinstance(other, KAO2_ePoint3):
            return KAO2_ePoint3 (
                self.x - other.x,
                self.y - other.y,
                self.z - other.z )

        return None

    def __mul__(self, other) -> "KAO2_ePoint3":

        if isinstance(other, (int, float)):
            return KAO2_ePoint3 (
                self.x * other,
                self.y * other,
                self.z * other )

        elif isinstance(other, KAO2_eQuat):
            result = KAO2_ePoint3()
            result.x \
                = (1.0 - (2 * other.z * other.z + 2 * other.y * other.y)) * self.x \
                + (2 * other.y * other.x + 2 * other.z * other.w) * self.y \
                + (2 * other.z * other.x - 2 * other.y * other.w) * self.z
            result.y \
                = (2 * other.y * other.x - 2 * other.z * other.w) * self.x \
                + (1.0 - (2 * other.z * other.z + 2 * other.x * other.x)) * self.y \
                + (2 * other.z * other.y + 2 * other.x * other.w) * self.z
            result.z \
                = (2 * other.z * other.x + 2 * other.y * other.w) * self.x \
                + (2 * other.z * other.y - 2 * other.x * other.w) * self.y \
                + (1.0 - (2 * other.x * other.x + 2 * other.y * other.y)) * self.z
            return result

        return None

    def getLength(self) -> float:

        return sqrt (
            self.x * self.x +
            self.y * self.y +
            self.z * self.z )

    def normalize(self) -> None:

        length = self.getLength()

        if 0 != length:

            self.x = self.x / length
            self.y = self.y / length
            self.z = self.z / length

    def serialize(self, ar: "KAO2_Archive") -> None:

        self._serializeFloat(ar, "x")
        self._serializeFloat(ar, "y")
        self._serializeFloat(ar, "z")

class KAO2_ePoint4(KAO2_Serializable):

    def __init__(self, x: float = 0, y: float = 0, z: float = 0, w: float = 0) -> None:

        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __eq__(self, other) -> bool:

        if isinstance(other, KAO2_ePoint4):
            return \
                (self.x == other.x) and \
                (self.y == other.y) and \
                (self.z == other.z) and \
                (self.w == other.w)

        return False

    def __add__(self, other) -> "KAO2_ePoint4":

        if isinstance(other, KAO2_ePoint4):
            return KAO2_ePoint4 (
                self.x + other.x,
                self.y + other.y,
                self.z + other.z,
                self.w + other.w )

        return None

    def __mul__(self, scalar) -> "KAO2_ePoint4":

        if isinstance(scalar, (int, float)):
            return KAO2_ePoint4 (
                self.x * scalar,
                self.y * scalar,
                self.z * scalar,
                self.w * scalar )

        return None

    def getLength(self) -> float:

        return sqrt (
            self.x * self.x +
            self.y * self.y +
            self.z * self.z +
            self.w * self.w )

    def normalize(self) -> None:

        length = self.getLength()

        if 0 != length:

            self.x = self.x / length
            self.y = self.y / length
            self.z = self.z / length
            self.w = self.w / length

    def serialize(self, ar: "KAO2_Archive") -> None:

        self._serializeFloat(ar, "x")
        self._serializeFloat(ar, "y")
        self._serializeFloat(ar, "z")
        self._serializeFloat(ar, "w")

class KAO2_ePhyVertex(KAO2_Serializable):

    def __init__(self) -> None:

        self.index = [0x80, 0x80, 0x80]
        self.weight = [0, 0, 0]

    def serialize(self, ar: "KAO2_Archive") -> None:

        assert 3 == len(self.index)
        self._serializeUInt8Array(ar, "index", False)

        ar.file.parseUInt8([0x80])

        assert 3 == len(self.weight)
        self._serializeFloatArray(ar, "weight", False)


class KAO2_eABB(KAO2_Serializable):

    def __init__(self, left_node: int = 0x80000000, right_node: int = 0xC0000001) -> None:

        self.min = KAO2_ePoint3()
        self.leftNode = left_node
        self.max = KAO2_ePoint3()
        self.rightNode = right_node

    def serialize(self, ar: "KAO2_Archive") -> None:

        self.min.serialize(ar)

        self._serializeUInt32(ar, "leftNode")

        self.max.serialize(ar)

        self._serializeUInt32(ar, "rightNode")


class KAO2_eQuat(KAO2_Serializable):

    def __init__(self, x: float = 0, y: float = 0, z: float = 0, w: float = 1.0) -> None:

        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __eq__(self, other) -> bool:

        if isinstance(other, KAO2_eQuat):
            return \
                (self.x == other.x) and \
                (self.y == other.y) and \
                (self.z == other.z) and \
                (self.w == other.w)

        return False

    def __mul__(self, other) -> "KAO2_eQuat":

        if isinstance(other, KAO2_eQuat):
            return KAO2_eQuat (
                self.y * other.z - self.z * other.y + self.w * other.x + other.w * self.x,
                self.z * other.x - self.x * other.z + self.w * other.y + other.w * self.y,
                self.x * other.y - self.y * other.x + self.w * other.z + other.w * self.z,
                self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z )

        return None

    def getLength(self) -> float:

        return sqrt (
            self.x * self.x +
            self.y * self.y +
            self.z * self.z +
            self.w * self.w )

    def normalize(self) -> None:

        length = self.getLength()

        if 0 != length:

            self.x = self.x / length
            self.y = self.y / length
            self.z = self.z / length
            self.w = self.w / length

        else:

            self.w = 1.0

    def inverse(self) -> None:

        self.x = - self.x
        self.y = - self.y
        self.z = - self.z

    @staticmethod
    def fromEulerAngles(alpha, beta, gamma) -> "KAO2_eQuat":

        alpha /= 2.0
        beta  /= 2.0
        gamma /= 2.0

        s1 = sin(alpha)
        s2 = sin(beta)
        s3 = sin(gamma)
        c1 = cos(alpha)
        c2 = cos(beta)
        c3 = cos(gamma)

        return KAO2_eQuat (
            c2 * c3 * s1 - c1 * s2 * s3,
            c2 * s1 * s3 + c1 * c3 * s2,
            c1 * c2 * s3 - c3 * s1 * s2,
            c1 * c2 * c3 + s1 * s2 * s3 )

    def serialize(self, ar: "KAO2_Archive") -> None:

        self._serializeFloat(ar, "x")
        self._serializeFloat(ar, "y")
        self._serializeFloat(ar, "z")
        self._serializeFloat(ar, "w")


class KAO2_eMatrix4x4(KAO2_Serializable):

    def __init__(self, mat: List[List[float]] = None) -> None:

        if mat is not None:
            self.m = mat
        else:
            self.m = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

    def __eq__(self, other) -> bool:

        if isinstance(other, KAO2_eMatrix4x4):
            for i in range (0, 4):
                for j in range (0, 4):
                    if self.m[i][j] != other.m[i][j]:
                        return False
            return True

        return False

    def __matmul__ (self, b):

        if isinstance(b, KAO2_eMatrix4x4):
            result = KAO2_eMatrix4x4()
            result.fromBlenderMatrix(Matrix(self.m) @ Matrix(b.m))
            return result

        elif isinstance(b, KAO2_ePoint4):
            vec = Matrix(self.m) @ Vector((b.x, b.y, b.z, b.w))
            return KAO2_ePoint4(vec.x, vec.y, vec.z, vec.w)

        return None

    def serialize(self, ar: "KAO2_Archive") -> None:

        # "INV_BIND_MATRIX" is stored as a transposed matrix (possibly for "OpenGL" compatibility)
        for row in range(0, 4):
            for column in range(0, 4):
                test = [self.m[column][row]]
                ar.file.parseFloat(test)
                self.m[column][row] = test[0]

    def fromBlenderMatrix(self, mat: Matrix) -> None:

        for i in range (0, 4):
            for j in range (0, 4):
                self.m[i][j] = mat[i][j]


class KAO2_eSRP(KAO2_Serializable):

    def __init__(self, scl: float = None, rot: KAO2_eQuat = None, pos: KAO2_ePoint3 = None) -> None:

        self.rot = rot if (rot is not None) else KAO2_eQuat()
        self.pos = pos if (pos is not None) else KAO2_ePoint3()
        self.scl = scl if (scl is not None) else 1.0

    def toBlenderVectors(self) -> Tuple[Vector, Quaternion, Vector]:

            pos = Vector ((
                self.pos.x,
                self.pos.y,
                self.pos.z ))

            rot = Quaternion ((
                self.rot.w,
                - self.rot.x,
                - self.rot.y,
                - self.rot.z ))

            scl = Vector ((
                self.scl,
                self.scl,
                self.scl ))

            return scl, rot, pos

    def fromMatrix(self, mat: KAO2_eMatrix4x4) -> Tuple[Vector, Quaternion, Vector]:

        pos, rot, scl = Matrix(mat.m).decompose()

        self.pos = KAO2_ePoint3(pos.x, pos.y, pos.z)
        self.rot = KAO2_eQuat(- rot.x, - rot.y, - rot.z, rot.w)
        self.scl = (scl.x + scl.y + scl.y) / 3.0

        return pos, rot, scl

    def getMatrix(self) -> KAO2_eMatrix4x4:

        result = KAO2_eMatrix4x4()

        invquat_x = - self.rot.x
        invquat_y = - self.rot.y
        invquat_z = - self.rot.z
        invquat_w = self.rot.w

        # (Translation x (Rotation x (Scale x Vector)))

        result.m[0][0] = self.scl * (1 - 2 * (invquat_y * invquat_y + invquat_z * invquat_z))
        result.m[0][1] = self.scl * (2 * (invquat_x * invquat_y - invquat_z * invquat_w))
        result.m[0][2] = self.scl * (2 * (invquat_x * invquat_z + invquat_y * invquat_w))
        result.m[0][3] = self.pos.x

        result.m[1][0] = self.scl * (2 * (invquat_x * invquat_y + invquat_z * invquat_w))
        result.m[1][1] = self.scl * (1 - 2 * (invquat_x * invquat_x + invquat_z * invquat_z))
        result.m[1][2] = self.scl * (2 * (invquat_y * invquat_z - invquat_x * invquat_w))
        result.m[1][3] = self.pos.y

        result.m[2][0] = self.scl * (2 * (invquat_x * invquat_z - invquat_y * invquat_w))
        result.m[2][1] = self.scl * (2 * (invquat_y * invquat_z + invquat_x * invquat_w))
        result.m[2][2] = self.scl * (1 - 2 * (invquat_x * invquat_x + invquat_y * invquat_y))
        result.m[2][3] = self.pos.z

        return result

    def getInverseMatrix(self) -> KAO2_eMatrix4x4:

        result = KAO2_eMatrix4x4()

        inv_scl = (1.0 / self.scl) if (0 != self.scl) else 0

        result.m[0][0] = inv_scl * (1 - 2 * (self.rot.y * self.rot.y + self.rot.z * self.rot.z))
        result.m[0][1] = inv_scl * (2 * (self.rot.x * self.rot.y - self.rot.z * self.rot.w))
        result.m[0][2] = inv_scl * (2 * (self.rot.x * self.rot.z + self.rot.y * self.rot.w))

        result.m[1][0] = inv_scl * (2 * (self.rot.x * self.rot.y + self.rot.z * self.rot.w))
        result.m[1][1] = inv_scl * (1 - 2 * (self.rot.x * self.rot.x + self.rot.z * self.rot.z))
        result.m[1][2] = inv_scl * (2 * (self.rot.y * self.rot.z - self.rot.x * self.rot.w))

        result.m[2][0] = inv_scl * (2 * (self.rot.x * self.rot.z - self.rot.y * self.rot.w))
        result.m[2][1] = inv_scl * (2 * (self.rot.y * self.rot.z + self.rot.x * self.rot.w))
        result.m[2][2] = inv_scl * (1 - 2 * (self.rot.x * self.rot.x + self.rot.y * self.rot.y))

        result.m[0][3] = - (result.m[0][0] * self.pos.x + result.m[0][1] * self.pos.y + result.m[0][2] * self.pos.z)
        result.m[1][3] = - (result.m[1][0] * self.pos.x + result.m[1][1] * self.pos.y + result.m[1][2] * self.pos.z)
        result.m[2][3] = - (result.m[2][0] * self.pos.x + result.m[2][1] * self.pos.y + result.m[2][2] * self.pos.z)

        return result

    @staticmethod
    def mix(first: "KAO2_eSRP", second: "KAO2_eSRP") -> "KAO2_eSRP":

        # Second "eSRP" (from child xform) is applied
        # onto the First "eSRP" (from parent xform)

        result = KAO2_eSRP()

        result.rot = second.rot * first.rot
        result.pos = ((second.pos * first.rot) * first.scl) + first.pos
        result.scl = second.scl * first.scl

        return result

    def debugPrint(self, head: str) -> None:

        print("{} (({:.6f} {:.6f} {:.6f}) ({:.6f} {:.6f} {:.6f} {:.6f}) ({:.6f}))".format(head, self.pos.x, self.pos.y, self.pos.z, self.rot.x, self.rot.y, self.rot.z, self.rot.w, self.scl))

    def serialize(self, ar: "KAO2_Archive") -> None:

        self._serializeFloat(ar, "scl")
        self.rot.serialize(ar)
        self.pos.serialize(ar)


################################################################

from .Archive import KAO2_Archive


################################################################
