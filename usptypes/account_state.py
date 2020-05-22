from typing import Optional
from lbrtypes.account_state import AccountState as LibraAccountState
from usptypes.account_resourses import ExchangeResource, ReserveResource, ExchangeInfoResource
from lbrtypes.move_core.language_storage import StructTag, TypeTag

class AccountState(LibraAccountState):
    @classmethod
    def new(cls, account_state: LibraAccountState):
        ret = cls()
        ret.ordered_map = account_state.ordered_map
        return ret

    def get_exchange_resource(self, token_name, exchange_address, token_address=None) -> Optional[ExchangeResource]:
        type_tag = TypeTag("Struct", StructTag.new(token_address, token_name))
        resource = self.get(ExchangeResource.resource_path_for(type_tag, module_address=exchange_address))
        if resource:
            return ExchangeResource.deserialize(resource)

    def get_reserve_resource(self, token_name, token_address=None) -> Optional[ReserveResource]:
        type_tag = TypeTag("Struct", StructTag.new(token_address, token_name))
        resource = self.get(ReserveResource.resource_path_for(type_tag, module_address=self.get_account_address()))
        if resource:
            return ReserveResource.deserialize(resource)

    def get_exchange_info_resource(self) -> Optional[ExchangeInfoResource]:
        resource = self.get(ExchangeInfoResource.resource_path_for(module_address=self.get_account_address()))
        if resource:
            return ExchangeInfoResource.deserialize(resource)
