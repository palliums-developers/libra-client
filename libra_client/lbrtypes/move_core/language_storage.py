from canoser import Struct, RustEnum, BoolT, Uint8, Uint64, Uint128
from lbrtypes.move_core.account_address import AccountAddress
from lbrtypes.move_core.identifier import Identifier
from crypto.hash import gen_hasher


CODE_TAG = 0
RESOURCE_TAG = 1

CORE_CODE_ADDRESS: AccountAddress = AccountAddress.default()

def core_code_address():
    return CORE_CODE_ADDRESS


class TypeTag(RustEnum):
    _enums = [
        ("Bool", BoolT),
        ("U8", Uint8),
        ("U64", Uint64),
        ("U128", Uint128),
        ("Address", AccountAddress),
        ("Signer", bytes),
        ("Vector", "lbrtypes.move_core.language_storage.TypeTag"),
        ("Struct", "lbrtypes.move_core.language_storage.StructTag")
    ]

class StructTag(Struct):
    _fields = [
        ("address", AccountAddress),
        ("module", Identifier),
        ("name", Identifier),
        ("type_params", [TypeTag])
    ]

    def hash(self):
        shazer = gen_hasher(b"StructTag")
        shazer.update(self.serialize())
        return shazer.digest()

    def get_address(self):
        return self.address.hex()

    def get_module(self):
        return self.module

    def get_name(self):
        return self.name

    def get_type_params(self):
        return self.type_params

    @classmethod
    def new(cls, module_address, module_name, struct_name=None, type_params=None):
        if module_address is None:
            module_address = CORE_CODE_ADDRESS
        if struct_name is None:
            struct_name = "T"
        if type_params is None:
            type_params = []
        if module_name is None:
            module_name = "LBR"
        ret = cls()
        ret.address = AccountAddress.normalize_to_bytes(module_address)
        ret.module = module_name
        ret.name = struct_name
        ret.type_params = type_params
        return ret


class ResourceKey(Struct):
    _fields = [
        ("address", AccountAddress),
        ("type_", StructTag)
    ]

class ModuleId(Struct):
    _fields = [
        ("address", AccountAddress),
        ("name", Identifier)
    ]

    def get_address(self):
        return self.address.hex()

    def get_name(self):
        return self.name

    def hash(self):
        shazer = gen_hasher(b"ModuleId")
        shazer.update(self.serialize())
        return shazer.digest()




