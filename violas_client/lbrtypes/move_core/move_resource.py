from lbrtypes.move_core.language_storage import StructTag
from lbrtypes.access_path import AccessPath, Accesses

class MoveResource():
    MODULE_NAME: str
    STRUCT_NAME: str

    @classmethod
    def module_identifier(cls):
        return cls.MODULE_NAME

    @classmethod
    def struct_identifier(cls):
        return cls.STRUCT_NAME

    @classmethod
    def type_params(cls):
        return []

    @classmethod
    def struct_tag(cls, *type_params, module_address=None):
        from lbrtypes.account_config import CORE_CODE_ADDRESS
        from lbrtypes.move_core.account_address import AccountAddress
        if module_address is None:
            module_address = CORE_CODE_ADDRESS
        module_address = AccountAddress.normalize_to_bytes(module_address)
        return StructTag(
            module_address,
            cls.module_identifier(),
            cls.struct_identifier(),
            list(type_params)
        )

    @classmethod
    def resource_path(cls):
        return AccessPath.resource_access_vec(cls.struct_tag(), Accesses.empty())

    @classmethod
    def resource_path_for(cls, *type_params, module_address=None):
        return AccessPath.resource_access_vec(cls.struct_tag(*type_params, module_address=module_address), Accesses.empty())
