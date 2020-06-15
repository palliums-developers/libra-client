from lbrtypes.move_core.language_storage import ModuleId, CORE_CODE_ADDRESS, StructTag, TypeTag

LIBRA_MODULE_NAME = "Libra"
COIN_MODULE_NAME = "Libra"
COIN_STRUCT_NAME = "T"
COIN_MODUL = ModuleId(CORE_CODE_ADDRESS, COIN_MODULE_NAME)

def coin_module_name():
    return COIN_MODULE_NAME

def coin_struct_name():
    return COIN_STRUCT_NAME


def type_tag_for_currency_code(currency_code, code_address=None) -> TypeTag:
    from lbrtypes.move_core.account_address import AccountAddress
    if code_address is None:
        code_address = CORE_CODE_ADDRESS
    code_address = AccountAddress.normalize_to_bytes(code_address)
    return TypeTag("Struct", StructTag(
        code_address,
        currency_code,
        coin_struct_name(),
        [])
    )

def from_currency_code_string(currency_code_string):
    return currency_code_string