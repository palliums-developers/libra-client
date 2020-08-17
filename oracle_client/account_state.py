from copy import deepcopy
from oracle_client.oracle_resource import OracleResource
from lbrtypes.account_state import AccountState as LibraAccountState

class AccountState(LibraAccountState):

    @classmethod
    def new(cls, account_state: LibraAccountState):
        ret = deepcopy(account_state)
        ret.__class__ = cls
        return ret

    def oracle_get_exchange_rate(self):
        resource = self.get(OracleResource.resource_path())
        return OracleResource.deserialize(resource)