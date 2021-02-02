################################################################
# "KAO2/eEnvironment.py"

import bpy
from mathutils import Matrix

from ..KaoUtility import *

from .eGroup import (KAO2_eGroup, KAO2_E_GROUP_TYPEINFO)

class KAO2_eEnvironment(KAO2_eGroup):

    def __init__(self) -> None:

        KAO2_eGroup.__init__(self)

        self.lights = []
        self.unknown_54 = [0, 0, 0, 1.0]
        self.fog = None

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_ENVIRONMENT_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        KAO2_eGroup.serialize(self, ar)

        self._serializeRefObjectArray(ar, "lights", KAO2_E_LIGHT_TYPEINFO)

        assert 4 == len(self.unknown_54)
        self._serializeFloatArray(ar, "unknown_54", False)

        if 0x1000 & self.flags:
            self._serializeRefObject(ar, "fog", KAO2_E_FOGENV_TYPEINFO)


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_ENVIRONMENT_TYPEINFO = KAO2_TypeInfo (
    0x3F800001,
    "eEnvironment",
    KAO2_E_GROUP_TYPEINFO,
    lambda: KAO2_eEnvironment()
)

from .eLight import KAO2_E_LIGHT_TYPEINFO
from .eFogEnv import KAO2_E_FOGENV_TYPEINFO


################################################################
