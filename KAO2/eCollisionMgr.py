################################################################
# "KAO2/eCollisionMgr.py"

from .eObject import KAO2_eObject

class KAO2_eCollisionMgr(KAO2_eObject):

    def __init__(self) -> None:

        self.seriesA = []
        self.unknown_10 = 0
        self.seriesB = []

    def serialize(self, ar: "KAO2_Archive") -> None:

        self._serializeUInt32Array(ar, "seriesA", True)
        self._serializeUInt32(ar, "unknown_10")


################################################################

from .Archive import KAO2_Archive


################################################################
