from canoser import Struct
from lbrtypes.move_core.move_resource import MoveResource
from lbrtypes.move_core.language_storage import StructTag, CORE_CODE_ADDRESS, TypeTag

class RegisteredCurrenciesResource(Struct, MoveResource):
    MODULE_NAME = "LibraConfig"
    STRUCT_NAME = "T"
    TYPE_TAG = TypeTag("Struct", StructTag(CORE_CODE_ADDRESS, "RegisteredCurrencies", "T", []))

    _fields = [
        ("currency_codes", [str])
    ]

    def __len__(self):
        return len(self.currency_codes)

    def __getitem__(self, item):
        return self.currency_codes[item]