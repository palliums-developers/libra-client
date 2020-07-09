from canoser import Struct, Uint64
from lbrtypes.account_config import LibraResource
from lbrtypes.event import EventHandle
from move_core_types.account_address import AccountAddress
from move_core_types.move_resource import MoveResource

class LibraTokenResource(Struct, MoveResource):
    MODULE_NAME = "ViolasBank"
    STRUCT_NAME = "LibraToken"

    _fields = [
        ("coin", LibraResource),
        ("index", Uint64)
    ]

    def get_libra_amount(self):
        return self.coin.value

    def get_index(self):
        return self.index

class BankResource(Struct):

    _fields = [
        ("index", Uint64),
        ("value", Uint64)
    ]

    def get_index(self):
        return self.index

    def get_value(self):
        return self.value

class BorrowInfoResource(Struct):
    _fields = [
        ("principal", Uint64),
        ("interest_index", Uint64)
    ]

    def get_principal(self):
        return self.principal

    def get_interest_index(self):
        return self.interest_index

class TokensResource(Struct, MoveResource):
    MODULE_NAME = "ViolasBank"
    STRUCT_NAME = "Tokens"

    _fields = [
        ("ts", [BankResource]),
        ("borrows", [BorrowInfoResource])
    ]


class OrderResource(Struct):

    _fields = [
        ("t", BankResource),
        ("peer_token_idx", Uint64),
        ("peer_token_amount", Uint64)
    ]

class UserInfoResource(Struct, MoveResource):
    MODULE_NAME = "ViolasBank"
    STRUCT_NAME = "UserInfo"

    _fields = [
        ("violas_events", EventHandle),
        ("data", str),
        ("orders", [OrderResource]),
        ("order_freeslots", [Uint64]),
        ("debug", str)
    ]

class TokenInfoResource(Struct):
    _fields = [
        ("currency_code", str),
        ("owner", AccountAddress),
        ("total_supply", Uint64),
        ("total_reserves", Uint64),
        ("total_borrows", Uint64),
        ("borrow_index", Uint64),
        ("price", Uint64),
        ("price_oracle", AccountAddress),
        ("collateral_factor", Uint64),
        ("last_minute", Uint64),
        ("data", str),
        ("bulletin_first", str),
        ("bulletins", [str]),
    ]

class TokenInfoStoreResource(Struct, MoveResource):
    MODULE_NAME = "ViolasBank"
    STRUCT_NAME = "TokenInfoStore"

    _fields = [
        ("supervisor", AccountAddress),
        ("tokens", [TokenInfoResource])
    ]

