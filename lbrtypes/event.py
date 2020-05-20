from canoser import Struct, Uint64, DelegateT, BytesT
from lbrtypes.move_core.account_address import AccountAddress

class EventKey(DelegateT):
    LENGTH = AccountAddress.LENGTH + 8
    delegate_type = BytesT(LENGTH)


class EventHandle(Struct):
    _fields = [
        ("count", Uint64),
        ("key", EventKey)
    ]

    def get_count(self):
        return self.count

    def get_key(self):
        return self.key

    def get_creator_address(self):
        return self.key[EventKey.LENGTH - AccountAddress.LENGTH:]