from lbrtypes.transaction.module import Module as LibraModule
from lbrtypes.move_core.account_address import AccountAddress as Address
from cmpdtypes.bytecode import get_code, CodeType

class Module(LibraModule):
    @staticmethod
    def gen_module(module_address):
        module_address = Address.normalize_to_bytes(module_address)
        code = get_code(CodeType.BANK, module_address)
        return Module(code)