from canoser import Struct, Uint64, Optional
from lbrtypes.event import EventHandle
from move_core_types.move_resource import MoveResource

class AccountResource(Struct, MoveResource):
    from lbrtypes.account_config.constants.account import ACCOUNT_MODULE_NAME
    from lbrtypes.account_config.resources import KeyRotationCapabilityResource, WithdrawCapabilityResource
    MODULE_NAME = ACCOUNT_MODULE_NAME
    STRUCT_NAME = ACCOUNT_MODULE_NAME

    _fields = [
        ("authentication_key", bytes),
        ("withdrawal_capability", Optional.from_type(WithdrawCapabilityResource)),
        ("key_rotation_capability", Optional.from_type(KeyRotationCapabilityResource)),
        ("received_events", EventHandle),
        ("sent_events", EventHandle),
        ("sequence_number", Uint64),
        ("is_frozen", bool),
        ("role_id", Uint64)
    ]


