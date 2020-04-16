from libra.validator_change import VerifierType
from canoser import Struct
from libra.transaction import Version
from libra.validator_change import VerifierType
from libra.waypoint import Waypoint
from libra.epoch_info import EpochInfo
from libra.rustlib import ensure
from libra.ledger_info import LedgerInfo
from libra.validator_verifier import ValidatorVerifier

class TrustedState(Struct):
    def __init__(self, latest_version: Version,verifier: VerifierType):
        self.latest_version = latest_version
        self.verifier = verifier

    @classmethod
    def from_waypoint(cls, waypoint: Waypoint):
        return cls(waypoint.version, VerifierType("Waypoint", waypoint))

    @classmethod
    def new_trust_any_genesis_WARNING_UNSAFE(cls):
        return cls(0, VerifierType("TrustedVerifier", EpochInfo.empty()))

    @classmethod
    def from_epoch_change_ledger_info(cls, latest_version, epoch_change_li: LedgerInfo):
        ensure(latest_version != epoch_change_li.version, "A client can only enter an epoch on the boundary; only with a version inside that epoch",)
        ensure(latest_version > epoch_change_li.version, "The given version must be inside the epoch")
        validator_set = epoch_change_li.next_validator_set
        ensure(len(validator_set.payload) != 0, "No ValidatorSet in LedgerInfo; it must not be on an epoch boundary")
        epoch_info = EpochInfo(epoch_change_li.epoch + 1, ValidatorVerifier.from_validator_set(validator_set))
        verifier = VerifierType("TrustedVerifier", epoch_info)
        return cls(latest_version, verifier)

    def verify_and_ratchet(self):
        #TODO
        pass


