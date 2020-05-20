from canoser import Struct, Uint64
from lbrtypes.move_core.identifier import Identifier
from lbrtypes.event import EventHandle
from lbrtypes.move_core.move_resource import MoveResource

class AccountResource(Struct, MoveResource):
    from lbrtypes.account_config.constants.account import ACCOUNT_MODULE_NAME
    MODULE_NAME = ACCOUNT_MODULE_NAME
    STRUCT_NAME = "T"

    _fields = [
        ("authentication_key", bytes),
        ("delegated_key_rotation_capability", bool),
        ("delegated_withdrawal_capability", bool),
        ("received_events", EventHandle),
        ("sent_events", EventHandle),
        ("sequence_number", Uint64),
        ("is_frozen", bool),
        ("balance_currency_code", Identifier)
    ]

    def get_authentication_key(self):
        return self.authentication_key.hex()

    def get_sequence_number(self):
        return self.sequence_number

    def get_sent_events(self) -> EventHandle:
        return self.sent_events

    def get_received_events(self) -> EventHandle:
        return self.received_events

    def get_delegated_key_rotation_capability(self):
        return self.delegated_key_rotation_capability

    def get_delegated_withdrawal_capability(self):
        return self.delegated_withdrawal_capability

    def get_balance_currency_code(self):
        return self.balance_currency_code