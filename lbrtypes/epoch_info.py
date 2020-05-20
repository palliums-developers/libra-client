from canoser import Struct, Uint64, RustOptional
from lbrtypes.validator_verifier import ValidatorVerifier

class EpochInfo(Struct):
    _fields = [
        ("epoch", Uint64),
        ("verifier", ValidatorVerifier)
    ]

    @classmethod
    def empty(cls):
        return cls(0, ValidatorVerifier.new({}))

class EpochInfoOptional(RustOptional):
    _type = EpochInfo