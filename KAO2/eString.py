################################################################
# "KAO2/eString.py"

class KAO2_eString(object):

    def __init__(self, text: str = "") -> None:

        self.text = text


    def readString(self, ar: "KAO2_Archive") -> None:

        test = []
        ar.file.parseUInt32(test)

        ar.file.parseBytes(test, test[0])
        self.text = test[0].decode("windows-1250")

        print("[KAO2] eString: \"{}\"".format(self.text))

    def writeString(self, ar: "KAO2_Archive") -> None:

        temp_bytes = [self.text.encode("windows-1250")]

        test = [len(temp_bytes[0])]
        ar.file.parseUInt32(test)

        ar.file.parseBytes(temp_bytes, test[0])


################################################################

from .Archive import KAO2_Archive


################################################################
