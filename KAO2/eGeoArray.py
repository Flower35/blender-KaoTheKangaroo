################################################################
# "KAO2/eGeoArray.py"

from .Basic import (KAO2_eUInt16, KAO2_ePoint2, KAO2_ePoint4, KAO2_eABB, KAO2_ePhyVertex)
from .eRefCounter import (KAO2_eRefCounter, KAO2_E_REFCOUNTER_TYPEINFO)

from typing import List

class KAO2_eGeoArray(KAO2_eRefCounter):

    E_3FXARRAY_ID = 0xEEEEEEDF

    def __init__(self, subclass_type: type) -> None:

        if subclass_type not in (KAO2_eUInt16, KAO2_ePoint2, KAO2_ePoint4, KAO2_eABB, KAO2_ePhyVertex):
            raise Exception("[KAO2] eGeoArray::__init__():\n\t" + "Invalid subclass type!")

        self._subclass_type = subclass_type

        self.data = []

    def getType(self: "KAO2_eCtrl") -> "KAO2_TypeInfo":

        if KAO2_eUInt16 is self._subclass_type:
            return KAO2_E_GEOARRAY_USHORT_TYPEINFO

        elif KAO2_ePoint2 is self._subclass_type:
            return KAO2_E_GEOARRAY_POINT2_TYPEINFO

        elif KAO2_ePoint4 is self._subclass_type:
            return KAO2_E_GEOARRAY_POINT4_TYPEINFO

        elif KAO2_eABB is self._subclass_type:
            return KAO2_E_GEOARRAY_ABB_TYPEINFO

        elif KAO2_ePhyVertex is self._subclass_type:
            return KAO2_E_GEOARRAY_PHYVERTEX_TYPEINFO

        return None

    def serialize(self, ar: "KAO2_Archive") -> None:

        self._serializeSerializables(ar, "data", self._subclass_type, None, True)

    @staticmethod
    def serialize_3fXArray(ar: "KAO2_Archive", obj: List["KAO2_eGeoAray"], index: int) -> None:

        if ar.isInReadMode:

            test = []
            ar.file.parseUInt32(test)

            if 0 == test[0]:

                ar.file.parseUInt32(test)

                if test[0] not in (KAO2_eGeoArray.E_3FXARRAY_ID, KAO2_E_GEOARRAY_POINT4_TYPEINFO.index):
                    raise Exception("[KAO2] e3fXArray::serialize():\n\t" + "Wrong object type in archive!\n\t" + "Expected: 0x{:08X} [e3fXArray] or 0x{:08X} [GeoArray<ePoint4>].".format(KAO2_eGeoArray.E_3FXARRAY_ID, KAO2_E_GEOARRAY_POINT4_TYPEINFO.index))

                obj[index] = KAO2_eGeoArray(KAO2_ePoint4)

                ar.addItem(obj[index], KAO2_Archive.ARCHIVE_ITEM_OBJECT)

                obj[index].serialize(ar)

            elif 1 == test[0]:

                obj[index] = None

            else:

                obj[index] = ar.getItem(test[0] - 2, KAO2_Archive.ARCHIVE_ITEM_OBJECT)

                if obj[index].getType() is not KAO2_E_GEOARRAY_POINT4_TYPEINFO:
                    raise Exception("[KAO2] e3fXArray::serialize():\n\t" + "Wrong object type in archive!\n\t" + "Expected: 0x{:08X} [eGeoArray<ePoint4>]\n\t".format(KAO2_E_GEOARRAY_POINT4_TYPEINFO.index) + "Current TypeInfo: 0x{08X} [{}]".format(new_info.index, new_info.name))

        else:

            if obj[index] is not None:

                test = ar.findItem(state[0])

                if test < 0:

                    ar.addItem(obj[index], KAO2_Archive.ARCHIVE_ITEM_OBJECT)

                    ar.file.parseUInt32([0])
                    ar.file.parseUInt32([KAO2_eGeoArray.E_3FXARRAY_ID if ar.version >= 0x89 else KAO2_E_GEOARRAY_POINT4_TYPEINFO.index])

                    obj[index].serialize(ar)

                else:

                    ar.file.parseUInt32([test + 2])

            else:

                ar.file.parseUInt32([1])


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_GEOARRAY_USHORT_TYPEINFO = KAO2_TypeInfo (
    0xEEEEEEE0,
    "eGeoArray<ushort>",
    KAO2_E_REFCOUNTER_TYPEINFO,
    lambda: KAO2_eGeoArray(KAO2_eUInt16)
)

KAO2_E_GEOARRAY_POINT2_TYPEINFO = KAO2_TypeInfo (
    0xEEEEEEE1,
    "eGeoArray<ePoint2>",
    KAO2_E_REFCOUNTER_TYPEINFO,
    lambda: KAO2_eGeoArray(KAO2_ePoint2)
)

KAO2_E_GEOARRAY_POINT4_TYPEINFO = KAO2_TypeInfo (
    0xEEEEEEE3,
    "eGeoArray<ePoint4>",
    KAO2_E_REFCOUNTER_TYPEINFO,
    lambda: KAO2_eGeoArray(KAO2_ePoint4)
)

KAO2_E_GEOARRAY_ABB_TYPEINFO = KAO2_TypeInfo (
    0xEEEEEEE4,
    "eGeoArray<eABB>",
    KAO2_E_REFCOUNTER_TYPEINFO,
    lambda: KAO2_eGeoArray(KAO2_eABB)
)

KAO2_E_GEOARRAY_PHYVERTEX_TYPEINFO = KAO2_TypeInfo (
    0xEEEEEEE5,
    "eGeoArray<ePhyVertex>",
    KAO2_E_REFCOUNTER_TYPEINFO,
    lambda: KAO2_eGeoArray(KAO2_ePhyVertex)
)


################################################################
