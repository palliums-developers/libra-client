from canoser import Struct, Uint64

class LibraVersion(Struct):
    _fields = [
        ("major", Uint64)
    ]