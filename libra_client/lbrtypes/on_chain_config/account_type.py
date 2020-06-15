from canoser import Struct, Uint64
from lbrtypes.move_core.account_address import AccountAddress


class RootVASP(Struct):
    _fields = [
        ("human_name", str),
        ("base_url", str),
        ("expiration_date", Uint64),
        ("ca_cert", bytes),
        ("travel_rule_public_key", bytes)
    ]

class ChildVASP(Struct):
    _fields = [
        ("is_certified", bool),
    ]


class RootVASPAccountType(Struct):
    _fields = [
        ("is_certified", bool),
        ("account_metadata", RootVASP),
        ("root_address", AccountAddress)
    ]

class EmptyAccountType(Struct):
    _fields = [
        ("is_certified", bool),
        ("account_metadata", bytes),
        ("root_address", AccountAddress)
    ]

class ChildVASPAccountType(Struct):
    _fields = [
        ("is_certified", bool),
        ("account_metadata", ChildVASP),
        ("root_address", AccountAddress)
    ]

class TransitionCapability(Struct):
    _fields = [
        ("is_certified", bool),
        ("root_address", AccountAddress)
    ]

class GrantingCapability(Struct):
    _fields = [
        ("is_certified", bool)
    ]
