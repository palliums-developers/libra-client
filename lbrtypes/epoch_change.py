from canoser import Struct, RustEnum
from lbrtypes.waypoint import Waypoint
from lbrtypes.epoch_info import EpochInfo
from lbrtypes.ledger_info import LedgerInfoWithSignatures

class EpochChangeProof(Struct):
    _fields = [
        ("ledger_info_with_sigs", [LedgerInfoWithSignatures]),
        ("more", bool)
    ]

    @classmethod
    def from_proto(cls, proto):
        ret = cls()
        ret.ledger_info_with_sigs = [LedgerInfoWithSignatures.deserialize(signature.bytes) for signature in proto.ledger_info_with_sigs]
        ret.more = proto.more
        return ret

class VerifierType(RustEnum):
    _enums = [
        ("Waypoint", Waypoint),
        ("TrustedVerifier", EpochInfo)
    ]

    def get_latest_version(self):
        if self.enum_name == "Waypoint":
            return self.value.version
        return 0
