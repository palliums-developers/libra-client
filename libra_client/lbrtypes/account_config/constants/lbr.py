from lbrtypes.move_core.language_storage import ModuleId, CORE_CODE_ADDRESS, TypeTag, StructTag
from lbrtypes.account_config.constants.libra import from_currency_code_string, coin_struct_name

LBR_NAME = "LBR"

LBR_MODULE = ModuleId(CORE_CODE_ADDRESS, LBR_NAME)
LBR_STRUCT_NAME = "T"

def lbr_type_tag() -> TypeTag:
    return TypeTag("Struct", StructTag(
        CORE_CODE_ADDRESS,
        from_currency_code_string(LBR_NAME),
        coin_struct_name(),
        [])
    )