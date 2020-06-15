from canoser import Struct, Uint64
from lbrtypes.move_core.identifier import Identifier
from lbrtypes.move_core.account_address import AccountAddress
from lbrtypes.move_core.move_resource import MoveResource
from lbrtypes.account_config.constants.libra import LIBRA_MODULE_NAME

class BurnEvent(Struct, MoveResource):
    MODULE_NAME  = LIBRA_MODULE_NAME
    STRUCT_NAME  = "BurnEvent"
    _fields = [
        ("amount", Uint64),
        ("currency_code", Identifier),
        ("preburn_address", AccountAddress),
    ]