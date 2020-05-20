from canoser import Struct
from lbrtypes.account_address import AccountAddress
from crypto.ed25519 import Ed25519PrivateKey

class ValidatorSigner(Struct):
    _fields = [
        ("author", AccountAddress),
        ("private_key", Ed25519PrivateKey)
    ]
