from canoser import Struct, RustEnum, Uint64
from lbrtypes.move_core.account_address import AccountAddress as Address
from crypto.ed25519 import Ed25519PublicKey
from lbrtypes.validator_info import ValidatorInfo

class VerifyError(RustEnum):
    _enums = [
        ("UnknownAuthor", None),
        ("TooLittleVotingPower", None),
        ("TooManySignatures", None),
        ("InvalidSignature", None),
    ]

class ValidatorConsensusInfo(Struct):
    _fields = [
        ("public_key", Ed25519PublicKey),
        ("voting_power", Uint64)
    ]

    def get_public_key(self):
        return self.public_key.hex()

    def get_voting_power(self):
        return self.voting_power


class ValidatorVerifier(Struct):
    _fields = [
        ('address_to_validator_info', {Address: ValidatorConsensusInfo}),
        ('quorum_voting_power', Uint64),
        ('total_voting_power', Uint64)
    ]

    @classmethod
    def new(cls, address_to_validator_info):
        ret = cls()
        ret.address_to_validator_info = address_to_validator_info
        ret.total_voting_power = sum(address_to_validator_info.values())
        if len(address_to_validator_info) == 0:
            ret.quorum_voting_power = 0
        else:
            ret.quorum_voting_power = ret.total_voting_power * 2 // 3 + 1
        return ret

    @classmethod
    def from_validator_set(cls, vset):
        pass



    def batch_verify_aggregated_signature(self, ledger_info_hash, signatures):
        pass

    def check_num_of_signatures(self, signatures):
        pass

    def check_voting_power(self, signatures):
        pass

    def get_voting_power(self, address):
        pass

    def check_keys(self, signatures):
        pass

    def verify_aggregated_signature(self, ledger_info_hash, signatures):
        pass

    def verify_signature(self, address, ledger_info_hash, signature):
        pass
