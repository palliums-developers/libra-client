from typing import Optional
from lbrtypes.account_state import AccountState as LibraAccountState
from usptypes.account_resources import ExchangeResource, ReserveResource, ExchangeInfoResource, RegisteredCurrenciesResource
from lbrtypes.move_core.language_storage import StructTag, TypeTag

class AccountState(LibraAccountState):
    @classmethod
    def new(cls, account_state: LibraAccountState):
        ret = cls()
        ret.ordered_map = account_state.ordered_map
        return ret

    def get_exchange_resource(self, token_name, exchange_module_address=None, token_module_address=None) -> Optional[ExchangeResource]:
        type_tag = TypeTag("Struct", StructTag.new(token_module_address, token_name))
        resource = self.get(ExchangeResource.resource_path_for(type_tag, module_address=self.get_exchange_module_address(exchange_module_address)))
        if resource:
            return ExchangeResource.deserialize(resource)

    def get_reserve_resource(self, token_name, token_module_address=None) -> Optional[ReserveResource]:
        type_tag = TypeTag("Struct", StructTag.new(token_module_address, token_name))
        resource = self.get(ReserveResource.resource_path_for(type_tag, module_address=self.get_account_address()))
        if resource:
            return ReserveResource.deserialize(resource)

    def get_exchange_info_resource(self) -> Optional[ExchangeInfoResource]:
        resource = self.get(ExchangeInfoResource.resource_path_for(module_address=self.get_account_address()))
        if resource:
            return ExchangeInfoResource.deserialize(resource)
        
    def get_liquidity_balance(self, token_reserve, violas_reserve, total_liquidity, token_name, token_module_address=None, exchange_module_address=None):
        liquidity_resource = self.get_exchange_resource(token_name, exchange_module_address=exchange_module_address, token_module_address=token_module_address)
        if liquidity_resource:
            liquidity_amount = liquidity_resource.get_amount()
            if total_liquidity == 0:
                return 0, 0, 0
            violas_amount = liquidity_amount * violas_reserve / total_liquidity
            token_amount = liquidity_amount * token_reserve / total_liquidity
            return liquidity_amount, violas_amount, token_amount
        
    def get_registered_currencies(self):
        resource = self.get(RegisteredCurrenciesResource.resource_path_for(module_address=self.get_account_address()))
        if resource:
            return RegisteredCurrenciesResource.deserialize(resource).currency_codes

    def is_contract_address(self):
        return self.get_registered_currencies() is not None

    def set_exchange_module_address(self, address):
        if address:
            self.exchange_module_address = address

    def get_exchange_module_address(self, address=None):
        if address:
            return address
        if hasattr(self, "exchange_module_address"):
            return self.exchange_module_address

