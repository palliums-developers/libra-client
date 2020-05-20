from canoser import Struct, DelegateT, Uint64
from lbrtypes.language_storage import StructTag, TypeTag
from lbrtypes.account_config import CORE_CODE_ADDRESS
from lbrtypes.access_path import AccessPath, Accesses
from lbrtypes.event import EventHandle
from lbrtypes.account_config import discovery_set_address
from lbrtypes.move_resource import MoveResource

class DiscoverySet(DelegateT):
    delegate_type = [DiscoveryInfo]

class DiscoverySetResource(Struct, MoveResource):
    MODULE_NAME = "LibraSystem"
    STRUCT_NAME = "DiscoverySet"

    _fields = [
        ("discovery_set", DiscoverySet),
        ("change_events", EventHandle)
    ]

class DiscoverySetChangeEvent(StructTag):
    _fields = [
        ("event_seq_num", Uint64),
        ("discovery_set", DiscoverySet)
    ]

DISCOVERY_SET_MODULE_NAME = "LibraSystem"
DISCOVERY_SET_STRUCT_NAME = "DiscoverySet"
DISCOVERY_SET_CHANGE_EVENT_STRUCT_NAME = "DiscoverySetChangeEvent"
DISCOVERY_SET_STRUCT_TAG = StructTag(
    DISCOVERY_SET_STRUCT_NAME,
    CORE_CODE_ADDRESS,
    DISCOVERY_SET_MODULE_NAME,
    []
)
DISCOVERY_SET_CHANGE_EVENT_STRUCT_TAG = StructTag(
    DISCOVERY_SET_CHANGE_EVENT_STRUCT_NAME,
    CORE_CODE_ADDRESS,
    DISCOVERY_SET_MODULE_NAME,
    []
)
DISCOVERY_SET_TYPE_TAG = TypeTag("Struct", DISCOVERY_SET_STRUCT_TAG)
DISCOVERY_SET_CHANGE_EVENT_TYPE_TAG = TypeTag("Struct", DISCOVERY_SET_CHANGE_EVENT_STRUCT_TAG)
DISCOVERY_SET_RESOURCE_PATH = AccessPath.resource_access_vec(DISCOVERY_SET_STRUCT_TAG, Accesses.empty())
DISCOVERY_SET_CHANGE_EVENT_PATH = DiscoverySetResource.resource_path() + b"/change_events_count/"
GLOBAL_DISCOVERY_SET_CHANGE_EVENT_PATH = AccessPath.new(discovery_set_address(), DISCOVERY_SET_CHANGE_EVENT_PATH)