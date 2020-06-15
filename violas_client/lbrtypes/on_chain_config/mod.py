from canoser import Struct, Uint64
from lbrtypes.event import EventHandle
from lbrtypes.move_core.account_address import AccountAddress
from lbrtypes.move_core.move_resource import MoveResource
from lbrtypes.access_path import AccessPath
from lbrtypes.move_core.language_storage import StructTag, CORE_CODE_ADDRESS, TypeTag

def config_address() -> AccountAddress:
    return AccountAddress.from_hex("0xF1A95")


def access_path_for_config(address, config_name: str) -> AccessPath:
    tag = StructTag(
        CORE_CODE_ADDRESS,
        config_name,
        "T",
        []
    )
    tag = StructTag(
        CORE_CODE_ADDRESS,
        "LibraConfig",
        "T",
        [TypeTag("Struct",tag)]
    )
    address = AccountAddress.normalize_to_bytes(address)
    return AccessPath(address, AccessPath.resource_access_vec(tag, []))

class ConfigID(Struct):
    _fields = [
        ("adddress", str),
        ("config_name", str)
    ]

    def access_path(self):
        return access_path_for_config(AccountAddress.from_hex(self.adddress), self.config_name)


class OnChainConfigPayload(Struct):
    _fields = [
        ("epoch", Uint64),
        ("configs", {ConfigID, bytes})
    ]

class OnChainConfig():
    ADDRESS = "0xF1A95"
    IDENTIFIER = ""
    CONFIG_ID = ConfigID(ADDRESS, IDENTIFIER)

class ConfigurationResource(Struct, MoveResource):
    MODULE_NAME = "LibraConfig"
    STRUCT_NAME = "Configuration"

    _fields = [
        ("epoch", Uint64),
        ("last_reconfiguration_time", Uint64),
        ("events", EventHandle)
    ]



class ChildVASPTransitionCapabilityResource(Struct, MoveResource):
    MODULE_NAME = "AccountType"
    STRUCT_NAME = "TransitionCapability"
    TYPE_TAG = TypeTag("Struct", StructTag(CORE_CODE_ADDRESS, "VASP", "ChildVASP", []))