from lbrtypes.move_core.language_storage import ModuleId, StructTag, TypeTag, CORE_CODE_ADDRESS
from canoser import Struct, Uint64
from lbrtypes.move_core.account_address import AccountAddress

ACCOUNT_TYPE_MODULE_NAME = "AccountType"
ACCOUNT_TYPE_MODULE = ModuleId(CORE_CODE_ADDRESS, ACCOUNT_TYPE_MODULE_NAME)
ACCOUNT_TYPE_STRUCT_NAME = "T"

VASP_TYPE_MODULE_NAME = "VASP"
VASP_TYPE_MODULE = ModuleId(CORE_CODE_ADDRESS, VASP_TYPE_MODULE_NAME)
ROOT_VASP_STRUCT_NAME = "RootVASP"
CHILD_VASP_STRUCT_NAME = "ChildVASP"


EMPTY_ACCOUNT_TYPE_MODULE_NAME = "Empty"
EMPTY_ACCOUNT_TYPE_MODULE = ModuleId(CORE_CODE_ADDRESS, EMPTY_ACCOUNT_TYPE_MODULE_NAME)
EMPTY_ACCOUNT_STRUCT_NAME = "T"

UNHOSTED_TYPE_MODULE_NAME = "Unhosted"
UNHOSTED_TYPE_MODULE = ModuleId(CORE_CODE_ADDRESS, UNHOSTED_TYPE_MODULE_NAME)
UNHOSTED_STRUCT_NAME = "T"

def account_type_module_name():
    return ACCOUNT_TYPE_MODULE_NAME


def account_type_struct_name():
    return ACCOUNT_TYPE_STRUCT_NAME


def transition_capability_struct_name():
    return "TransitionCapability"

def granting_capability_struct_name():
    return "GrantingCapability"

def update_capability_struct_name():
    return "UpdateCapability"

def registered_struct_name():
    return "Registered"

def vasp_type_module_name():
    return VASP_TYPE_MODULE_NAME

def root_vasp_type_struct_name():
    return ROOT_VASP_STRUCT_NAME

def child_vasp_type_struct_name():
    return CHILD_VASP_STRUCT_NAME


def empty_account_type_module_name():
    return EMPTY_ACCOUNT_TYPE_MODULE_NAME


def empty_account_type_struct_name():
    return EMPTY_ACCOUNT_STRUCT_NAME


def unhosted_type_module_name():
    return UNHOSTED_TYPE_MODULE_NAME


def unhosted_type_struct_name():
    return UNHOSTED_STRUCT_NAME


def empty_account_type_struct_tag() -> StructTag:
        inner_struct_tag = StructTag(
            CORE_CODE_ADDRESS,
            empty_account_type_module_name(),
            empty_account_type_struct_name(),
            [],
        )
        return StructTag(
            CORE_CODE_ADDRESS,
            account_type_module_name(),
            account_type_struct_name(),
            [TypeTag("Struct", inner_struct_tag)],

        )

def vasp_account_type_struct_tag() -> StructTag :
    inner_struct_tag = StructTag(
        CORE_CODE_ADDRESS,
        vasp_type_module_name(),
        root_vasp_type_struct_name(),
        [],

    )
    
    return StructTag(
        CORE_CODE_ADDRESS,
        account_type_module_name(),
        account_type_struct_name(),
        [TypeTag("Struct", inner_struct_tag)],
    )

def unhosted_account_type_struct_tag() -> StructTag :
    inner_struct_tag = StructTag(
        CORE_CODE_ADDRESS,
        unhosted_type_module_name(),
        unhosted_type_struct_name(),
        [],
    )
    return StructTag(
        CORE_CODE_ADDRESS,
        account_type_module_name(),
        account_type_struct_name(),
        [TypeTag("Struct", inner_struct_tag)]
    )


def child_vasp_account_type_struct_tag() -> StructTag:
    inner_struct_tag = StructTag(
        CORE_CODE_ADDRESS,
        vasp_type_module_name(),
        child_vasp_type_struct_name(),
        [],
    )
    return StructTag(
        CORE_CODE_ADDRESS,
        account_type_module_name(),
        account_type_struct_name(),
        [TypeTag("Struct", inner_struct_tag)]
    )

def child_vasp_transition_capability_struct_tag() ->StructTag:
    inner_struct_tag = StructTag(
        CORE_CODE_ADDRESS,
        vasp_type_module_name(),
        child_vasp_type_struct_name(),
        [],
    )

    return StructTag(
        CORE_CODE_ADDRESS,
        account_type_module_name(),
        transition_capability_struct_name(),
        [TypeTag("Struct", inner_struct_tag)]
    )

def root_vasp_transition_capability_struct_tag() ->StructTag:
    inner_struct_tag = StructTag(
        CORE_CODE_ADDRESS,
        vasp_type_module_name(),
        root_vasp_type_struct_name(),
        [],
    )

    return StructTag(
        CORE_CODE_ADDRESS,
        account_type_module_name(),
        transition_capability_struct_name(),
        [TypeTag("Struct", inner_struct_tag)]
    )



def child_vasp_granting_capability_struct_tag() -> StructTag:
    inner_struct_tag = StructTag(
        CORE_CODE_ADDRESS,
        vasp_type_module_name(),
        child_vasp_type_struct_name(),
        [],
    )

    return StructTag(
        CORE_CODE_ADDRESS,
        account_type_module_name(),
        granting_capability_struct_name(),
        [TypeTag("Struct", inner_struct_tag)]
    )

def root_vasp_granting_capability_struct_tag() -> StructTag:
    inner_struct_tag = StructTag(
        CORE_CODE_ADDRESS,
        vasp_type_module_name(),
        root_vasp_type_struct_name(),
        [],
    )

    return StructTag(
        CORE_CODE_ADDRESS,
        account_type_module_name(),
        granting_capability_struct_name(),
        [TypeTag("Struct", inner_struct_tag)]
    )




