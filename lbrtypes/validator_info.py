from canoser import Struct, Uint64
from lbrtypes.move_core.account_address import AccountAddress
from crypto.ed25519 import Ed25519PublicKey
from crypto.x25519 import PublicKey

class ValidatorInfo(Struct):
    _fields = [
        ("account_address", AccountAddress),
        ("consensus_public_key", Ed25519PublicKey),
        ("consensus_voting_power", Uint64),
        ("network_signing_public_key", Ed25519PublicKey),
        ("network_identity_public_key", PublicKey)
    ]