################################################################
# "KAO2/eScene.py"

from .ePivot import (KAO2_ePivot, KAO2_E_PIVOT_TYPEINFO)

class KAO2_eScene(KAO2_ePivot):

    def __init__(self) -> None:

        KAO2_ePivot.__init__(self)

        self.collision = KAO2_eCollisionMgr()
        self.backgroundColor = [0.5, 0.5, 0.5]
        self.ambientColor = [0, 0, 0, 1.0]
        self.compilerStringA = KAO2_eString()
        self.compilerStringB = KAO2_eString()
        self.unknown_0194 = []
        self.visGroups = []
        self.visGroupsUnknown = 0
        self.visSetA = []
        self.visSetB = []

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_SCENE_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        self._serializeString(ar, "compilerStringB")
        self._serializeString(ar, "compilerStringA")

        self.collision.serialize(ar)

        KAO2_ePivot.serialize(self, ar)

        assert 3 == len(self.backgroundColor)
        self._serializeFloatArray(ar, "backgroundColor", False)

        self._serializeRefObjectArray(ar, "unknown_0194", KAO2_E_PIVOT_TYPEINFO)

        assert 4 == len(self.ambientColor)
        self._serializeFloatArray(ar, "ambientColor", False)

        if ar.version >= 0x8C:

            self._serializeUInt8(ar, "visGroupsUnknown")

            self._serializeRefObjectArray(ar, "visGroups", KAO2_E_NODE_TYPEINFO)
            test = len(self.visGroups)
            if test > 512:
                raise Exception("[KAO2] eScene::serialize():\n\t" + "Too many visibility nodes/groups ({}/512).".format(test))

        if ar.version >= 0x8D:

            for i in range (0, 2):
                test = [0]
                ar.file.parseUInt32(test)
                if 0 != test[0]:
                    raise Exception("[KAO2] eScene::serialize():\n\t" + "visPortals are not supported!")


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_SCENE_TYPEINFO = KAO2_TypeInfo (
    0x8001,
    "eScene",
    KAO2_E_PIVOT_TYPEINFO,
    lambda: KAO2_eScene()
)

from .eString import KAO2_eString
from .eCollisionMgr import KAO2_eCollisionMgr
from .eNode import KAO2_E_NODE_TYPEINFO


################################################################
