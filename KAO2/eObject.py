################################################################
# "KAO2/eObject.py"

from .Basic import KAO2_Serializable

class KAO2_eObject(KAO2_Serializable):

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_OBJECT_TYPEINFO

    def _serializeRefObject(self, ar: "KAO2_Archive", prop_name: str, info: "KAO2_TypeInfo") -> None:

        test = [getattr(self, prop_name)]
        ar.serialize(test, 0, info)
        setattr(self, prop_name, test[0])

    def _serializeRefObjectArray(self, ar: "KAO2_Archive", array_name: str, info: "KAO2_TypeInfo") -> None:

        array = getattr(self, array_name)
        length = len(array)

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

            ar.serialize(array, i, info)


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_OBJECT_TYPEINFO = KAO2_TypeInfo (
    0x01,
    "eObject",
    None,
    lambda: KAO2_eObject()
)


################################################################
