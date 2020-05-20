from canoser import Struct, Uint64, RustOptional
from lbrtypes.transaction import Version
from crypto.hash import HashValue
from lbrtypes.epoch_info import EpochInfo

class Round(Uint64):
    pass

GENESIS_EPOCH = 0
GENESIS_ROUND = 0
GENESIS_VERSION = 0
GENESIS_TIMESTAMP_USECS = 0

class EpochInfoOptional(RustOptional):
    _type = EpochInfo


class BlockInfo(Struct):
    _fields = [
        ("epoch", Uint64),
        ("round", Round),
        ("id", HashValue),
        ("executed_state_id", HashValue),
        ("version", Version),
        ("timestamp_usecs", Uint64),
        ("next_epoch_info", EpochInfoOptional),
    ]