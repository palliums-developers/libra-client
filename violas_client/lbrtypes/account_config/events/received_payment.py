from canoser import Struct, Uint64
from lbrtypes.move_core.identifier import Identifier
from lbrtypes.move_core.account_address import AccountAddress
from lbrtypes.move_core.move_resource import MoveResource
from lbrtypes.account_config.constants.libra import LIBRA_MODULE_NAME
from lbrtypes.account_config.resources.account import AccountResource

ACCOUNT_RECEIVED_EVENT_PATH = AccountResource.resource_path() + b"/received_events_count/"

class ReceivedPaymentEvent(Struct, MoveResource):
    MODULE_NAME = LIBRA_MODULE_NAME
    STRUCT_NAME = "ReceivedPaymentEvent"

    _fields = [
        ("amount", Uint64),
        ("currency_code", Identifier),
        ("sender", AccountAddress),
        ("metadata", bytes),
    ]