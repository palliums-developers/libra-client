from lbrtypes.event import EventHandle
from canoser import Struct, Uint64
from move_core_types.move_resource import MoveResource


class DesignatedDealer(Struct, MoveResource):
    MODULE_NAME = "DesignatedDealer"
    STRUCT_NAME = "Dealer"

    _fields = [
        ("received_mint_events", EventHandle),
    ]

