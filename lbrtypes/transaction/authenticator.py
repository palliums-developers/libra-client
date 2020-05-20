from canoser import Struct, RustEnum
from enum import IntEnum

from crypto.ed25519 import Ed25519PublicKey, Ed25519Signature
from crypto.multi_ed25519 import MultiEd25519PublicKey, MultiEd25519Signature
from crypto.hash import HashValue

from lbrtypes.move_core.account_address import AccountAddress

class Scheme(IntEnum):
    Ed25519 = 0
    MultiEd25519 = 1

    def to_bytes(self):
        return super().to_bytes(1, "little")

class Ed25519(Struct):
    _fields = [
        ("public_key", Ed25519PublicKey),
        ("signature", Ed25519Signature)
    ]

class MultiEd25519(Struct):
    _fields = [
        ("public_key", MultiEd25519PublicKey),
        ("signature", MultiEd25519Signature),
    ]

class TransactionAuthenticator(RustEnum):
    _enums = [
        ("Ed25519", Ed25519),
        ("MultiEd25519", MultiEd25519)
    ]

    @classmethod
    def ed25519(cls, public_key: Ed25519PublicKey, signature: Ed25519Signature):
        return cls("Ed25519", Ed25519(public_key, signature))

class AuthenticationKeyPreimage(bytes):

    @classmethod
    def new(cls, public_key:bytes, scheme: Scheme):
        return AuthenticationKeyPreimage(public_key+scheme.to_bytes())

    @classmethod
    def ed25519(cls, public_key: Ed25519PublicKey):
        return cls.new(public_key, Scheme.Ed25519)

    @classmethod
    def multi_ed25519(cls, public_key: MultiEd25519PublicKey):
        return cls.new(public_key.to_bytes(), Scheme.MultiEd25519)

class AuthenticationKey(bytes):
    LENGTH = 32

    @classmethod
    def from_preimage(cls, preimage: AuthenticationKeyPreimage):
        return cls(HashValue.from_sha3_256(preimage))

    @classmethod
    def ed25519(cls, publick_key: Ed25519PublicKey):
        return cls.from_preimage(AuthenticationKeyPreimage.ed25519(publick_key))

    @classmethod
    def multi_ed25519(cls, public_key: MultiEd25519PublicKey):
        return cls.from_preimage(AuthenticationKeyPreimage.multi_ed25519(public_key))

    def derived_address(self) -> bytes:
        return self[(self.LENGTH - AccountAddress.LENGTH):]

    def prefix(self):
        return self[:AccountAddress.LENGTH]

    def short_str(self):
        return self[:4].hex()




