from canoser import Struct, Uint64
from lbrtypes.move_core.account_address import AccountAddress
from lbrtypes.validator_config import ValidatorConfig
from crypto.ed25519 import Ed25519PublicKey
from crypto.x25519 import PublicKey

class ValidatorInfo(Struct):
    _fields = [
        ("account_address", AccountAddress),
        ("consensus_voting_power", Uint64),
        ("config", ValidatorConfig)
    ]

    def get_account_address(self):
        return self.account_address.hex()

    def get_consensus_voting_power(self):
        return self.consensus_voting_power

    def get_network_identity_public_key(self):
        return self.config.network_identity_public_key.hex()

    def get_config(self):
        return self.config
