from canoser import Struct
from libra.validator_verifier import ValidatorVerifier

class EpochInfo(Struct):
    def __init__(self, epoch: int, verifier: ValidatorVerifier):
        self.epoch = epoch
        self.verifier = verifier

    @classmethod
    def empty(cls):
        return cls(0, ValidatorVerifier(dict()))

