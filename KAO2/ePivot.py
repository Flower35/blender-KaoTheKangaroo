################################################################
# "KAO2/ePivot.py"

import bpy

from ..KaoUtility import *

from .eTransform import (KAO2_eTransform, KAO2_E_TRANSFORM_TYPEINFO)

class KAO2_ePivot(KAO2_eTransform):

    def __init__(self) -> None:

        KAO2_eTransform.__init__(self)

        self.animations = KAO2_eAnimate()

        self.blenderActions = []

    def getType(self) -> "KAO2_TypeInfo":

        return KAO2_E_PIVOT_TYPEINFO

    def serialize(self, ar: "KAO2_Archive") -> None:

        KAO2_eTransform.serialize(self, ar)

        self.animations.serialize(ar)

        test = [0]
        ar.file.parseUInt32(test)
        if 0 != test[0]:
            raise Exception("[KAO2] ePivot::serialize():\n\t" + "non-empty group member is not supported!")

    def updateBlenderAnims(self) -> None:

        obj = self.blenderObj

        previous_actions = Settings.actionsList
        Settings.actionsList = []

        tracks_count = len(self.animations.tracks)
        if tracks_count > 0:
            if not obj.animation_data:
                obj.animation_data_create()

            for i in range (0, tracks_count):
                action = bpy.data.actions.new(name = self.animations.tracks[i].name.text)
                action.use_fake_user = True
                Settings.actionsList.append(action)

            obj.animation_data.action = Settings.actionsList[0]

        KAO2_eTransform.updateBlenderAnims(self)

        Settings.actionsList = previous_actions


################################################################

from .Archive import KAO2_Archive
from .TypeInfo import KAO2_TypeInfo

KAO2_E_PIVOT_TYPEINFO = KAO2_TypeInfo (
    0x00AA3456,
    "ePivot",
    KAO2_E_TRANSFORM_TYPEINFO,
    lambda: KAO2_ePivot()
)

from .eAnimate import KAO2_eAnimate


################################################################
