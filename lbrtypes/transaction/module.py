from canoser import Struct, Uint8
from lbrtypes.move_core.account_address import AccountAddress as Address
from lbrtypes.bytecode import get_code, CodeType

class Module(Struct):
    _fields = [
        ("code", bytes)
    ]

    def get_code(self):
        return self.code.hex()

    @classmethod
    def gen_module(cls, module_address):
        module_address = Address.normalize_to_bytes(module_address)
        code = get_code(CodeType.PUBLISH_MODULE, module_address)
        return Module(code)

