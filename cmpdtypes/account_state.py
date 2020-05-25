from lbrtypes.account_state import AccountState as LibraAccountState
from cmpdtypes.account_resources import TokensResource, UserInfoResource, TokenInfoStoreResource

class AccountState(LibraAccountState):

    @classmethod
    def new(cls, account_state: LibraAccountState):
        ret = cls()
        ret.ordered_map = account_state.ordered_map
        return ret

    def get_tokens_resource(self, bank_module_address=None):
        resource = self.ordered_map.get(TokensResource.resource_path_for(module_address=self.get_bank_module_address(bank_module_address)))
        if resource:
            return TokensResource.deserialize(resource)

    def get_user_info_resource(self, bank_module_address=None):
        resource = self.ordered_map.get(
            UserInfoResource.resource_path_for(module_address=self.get_bank_module_address(bank_module_address)))
        if resource:
            return UserInfoResource.deserialize(resource)

    def get_token_info_store_resource(self,bank_module_address=None):
        resource = self.ordered_map.get(
            TokenInfoStoreResource.resource_path_for(module_address=self.get_bank_module_address(bank_module_address)))
        if resource:
            return TokenInfoStoreResource.deserialize(resource)

    def set_bank_module_address(self, address):
        if address:
            self.bank_module_address = address

    def get_bank_module_address(self, address=None):
        if address:
            return address
        if hasattr(self, "bank_module_address"):
            return self.bank_module_address