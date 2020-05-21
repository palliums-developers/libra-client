from canoser import Struct, Uint64
from lbrtypes.account_config import LibraResource
from lbrtypes.event import EventHandle
from lbrtypes.move_core.move_resource import MoveResource

EXCHANGE_MODULE_NAME = "Exchange"

class ExchangeResource(Struct, MoveResource):
    MODULE_NAME = EXCHANGE_MODULE_NAME
    STRUCT_NAME = "T"

    _fields = [
        ("value", Uint64)
    ]

class ReserveResource(Struct, MoveResource):
    MODULE_NAME = EXCHANGE_MODULE_NAME
    STRUCT_NAME = "Reserve"

    _fields = [
        ("liquidity_total_supply", Uint64),
        ("token", LibraResource),
        ("violas", LibraResource),
    ]

    def get_liquidity_total_supply(self):
        return self.liquidity_total_supply

    def get_token_reource(self):
        return self.token

    def get_violas_resource(self):
        return self.violas

class ExchangeInfoResource(Struct, MoveResource):
    MODULE_NAME = EXCHANGE_MODULE_NAME
    STRUCT_NAME = "ExchangeInfo"

    _fields = [
        ("mint_events", EventHandle),
        ("burn_events", EventHandle),
        ("swap_events", EventHandle),
    ]