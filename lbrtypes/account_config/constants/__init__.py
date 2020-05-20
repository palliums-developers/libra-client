from .account_limits import *
from .account_type import *
from .addresses import *
from .debug import *
from .event import *
from .lbr import *
from .libra import *
from .account import *


def get_coin_type(module_address, module_name, struct_name):
    from lbrtypes.account_config.constants.lbr import LBR_NAME
    from lbrtypes.account_config.constants.libra import coin_struct_name

    if module_address is None:
        module_address = CORE_CODE_ADDRESS
    if module_name is None:
        module_name = LBR_NAME
    if struct_name is None:
        struct_name = coin_struct_name()
    module_address = AccountAddress.normalize_to_bytes(module_address)
    return TypeTag("Struct", StructTag(
        module_address,
        module_name,
        struct_name,
        []
    ))
