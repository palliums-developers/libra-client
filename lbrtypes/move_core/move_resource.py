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
        if hasattr(cls, "TYPE_TAG"):
            return [cls.TYPE_TAG]
        return []

    @classmethod
    def struct_tag(cls):
        from lbrtypes.account_config import CORE_CODE_ADDRESS
        return StructTag(
            CORE_CODE_ADDRESS,
            cls.module_identifier(),
            cls.struct_identifier(),
            cls.type_params()
        )

    @classmethod
    def resource_path(cls):
        return AccessPath.resource_access_vec(cls.struct_tag(), Accesses.empty())