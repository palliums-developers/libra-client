from canoser import Struct, Uint64
from move_core_types.move_resource import MoveResource

class RoleId(Struct, MoveResource):
    MODULE_NAME = "Roles"
    STRUCT_NAME = "RoleId"

    _fields = [
        ("role_id", Uint64)
    ]