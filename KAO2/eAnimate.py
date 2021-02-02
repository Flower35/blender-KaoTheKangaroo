################################################################
# "KAO2/eAnimate.py"

from typing import List

from .eObject import KAO2_eObject

class KAO2_eAnimate(KAO2_eObject):

    def __init__(self) -> None:

        self.tracks = []
        self.oldAnimStates = [None, None]
        self.isPaused = False
        self.unknown_34 = 0
        self.unknown_38 = False
        self.currentAnimState = KAO2_eAnimState()

    @staticmethod
    def serialize_AnimStates(ar: "KAO2_Archive", state: List[List["KAO2_eAnimState"]], index: int) -> None:

        if ar.isInReadMode:

            test = []
            ar.file.parseUInt32(test)

            if 0 == test[0]:

                state[index] = [None]

                ar.addItem(state[index], KAO2_Archive.ARCHIVE_ITEM_OTHER)

                for i in range (0, 2):
                    test = [1]
                    ar.file.parseUInt32(test)
                    if 1 != test[0]:
                        raise Exception("[KAO2] eAnimate::serialize():\n\t" + "resursive objects are not supported!")

                ar.serialize(state[index], 0, KAO2_E_ANIMSTATE_TYPEINFO)

            elif 1 == test[0]:

                state[index] = None

            else:

                state[index] = ar.getItem(test[0] - 2, KAO2_Archive.ARCHIVE_ITEM_OTHER)

        else:

            if state[index] is not None:

                test = ar.findItem(state[index])

                if test < 0:

                    ar.addItem(state[index], KAO2_Archive.ARCHIVE_ITEM_OTHER)

                    ar.file.parseUInt32([0])

                    for i in range (0, 2):
                        ar.file.parseUInt32([1])

                    ar.serialize(state[index], 0, KAO2_E_ANIMSTATE_TYPEINFO)

                else:

                    ar.file.parseUInt32([test + 2])

            else:

                ar.file.parseUInt32([1])

    def serialize(self, ar: "KAO2_Archive") -> None:

        if ar.version >= 0x8A:

            test = [1]
            ar.file.parseUInt32(test)
            if 1 != test[0]:
                raise Exception("[KAO2] eAnimate::serialize():\n\t" + "expected exactly one \"eAnimState\" object!")

            self.currentAnimState.serialize(ar)

            if ar.isInReadMode:

                self.oldAnimStates[0] = [self.currentAnimState]
                self.oldAnimStates[1] = self.oldAnimStates[0]

        else:

            if not ar.isInReadMode:

                self.oldAnimStates[0] = [self.currentAnimState]

            KAO2_eAnimate.serialize_AnimStates(ar, self.oldAnimStates, 0)
            KAO2_eAnimate.serialize_AnimStates(ar, self.oldAnimStates, 1)

            if ar.isInReadMode and (self.oldAnimStates[0] is not None):

                self.currentAnimState = self.oldAnimStates[0][0]

        self._serializeRefObjectArray(ar, "tracks", KAO2_E_TRACK_TYPEINFO)

        self._serializeUInt8(ar, "isPaused")
        self._serializeUInt32(ar, "unknown_34")
        self._serializeUInt8(ar, "unknown_38")


################################################################

from .Archive import KAO2_Archive

from .eTrack import KAO2_E_TRACK_TYPEINFO
from .eAnimState import (KAO2_eAnimState, KAO2_E_ANIMSTATE_TYPEINFO)


################################################################
