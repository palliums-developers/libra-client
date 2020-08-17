from canoser import Struct
from move_core_types.move_resource import MoveResource

class UpdateEvent(Struct):
    _fields = [
        ("value", int),
        ("timestamp ", int),
        ("currency_code ", str),
    ]

class OracleResource(Struct, MoveResource):
    MODULE_NAME = "Oracle"
    STRUCT_NAME = "ExchangeRate"

    _fields = [
        ("value", int),
        ("timestamp", int),
        ("update_events", UpdateEvent),
    ]