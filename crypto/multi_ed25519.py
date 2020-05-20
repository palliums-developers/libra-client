from canoser import Struct, Uint8
from crypto.ed25519 import Ed25519PrivateKey, Ed25519PublicKey, Ed25519Signature

MAX_NUM_OF_KEYS = 32
BITMAP_NUM_OF_BYTES = 4

class MultiEd25519PrivateKey(Struct):
    _fields = [
        ("private_keys", [Ed25519PrivateKey]),
        ("threshold", Uint8)
    ]

class MultiEd25519PublicKey(Struct):
    _fields = [
        ("public_keys", [Ed25519PublicKey]),
        ("threshold", Uint8)
    ]

    def to_bytes(self):
        ret = b""
        for publick_key in self.public_keys:
            ret += publick_key
        ret += self.threshold.to_bytes(1, "little")

class MultiEd25519Signature(Struct):
    _fields = [
        ("signatures", [Ed25519Signature]),
        ("threshold", [Uint8, BITMAP_NUM_OF_BYTES])
    ]

class Multiaddr(bytes):
    pass