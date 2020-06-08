from typing import Optional
from lbrtypes.account_state import AccountState as LibraAccountState
from extypes.account_resources import ExchangeResource, ReserveResource, ExchangeInfoResource, RegisteredCurrenciesResource
from lbrtypes.move_core.language_storage import StructTag, TypeTag
from error import get_exception

class AccountState(LibraAccountState):
    @classmethod
    def new(cls, account_state: LibraAccountState):
        ret = cls()
        ret.ordered_map = account_state.ordered_map
        return ret

    @get_exception
    def get_exchange_resource(self, token_name, exchange_module_address=None, token_module_address=None) -> Optional[ExchangeResource]:
        type_tag = TypeTag("Struct", StructTag.new(token_module_address, token_name))
        resource = self.get(ExchangeResource.resource_path_for(type_tag, module_address=self.get_exchange_module_address(exchange_module_address)))
        return ExchangeResource.deserialize(resource)

    @get_exception
    def get_reserve_resource(self, token_name, token_module_address=None) -> Optional[ReserveResource]:
        type_tag = TypeTag("Struct", StructTag.new(token_module_address, token_name))
        resource = self.get(ReserveResource.resource_path_for(type_tag, module_address=self.get_account_address()))
        return ReserveResource.deserialize(resource)

    @get_exception
    def get_exchange_info_resource(self) -> Optional[ExchangeInfoResource]:
        resource = self.get(ExchangeInfoResource.resource_path_for(module_address=self.get_account_address()))
        return ExchangeInfoResource.deserialize(resource)

    @get_exception
    def get_liquidity_balance(self, token_reserve, violas_reserve, total_liquidity, token_name, token_module_address=None, exchange_module_address=None):
        liquidity_resource = self.get_exchange_resource(token_name, exchange_module_address=exchange_module_address, token_module_address=token_module_address)
        liquidity_amount = liquidity_resource.get_amount()
        if total_liquidity == 0:
            return 0, 0, 0
        violas_amount = liquidity_amount * violas_reserve / total_liquidity
        token_amount = liquidity_amount * token_reserve / total_liquidity
        return liquidity_amount, violas_amount, token_amount

    @get_exception
    def get_registered_currencies(self):
        resource = self.get(RegisteredCurrenciesResource.resource_path_for(module_address=self.get_account_address()))
        return RegisteredCurrenciesResource.deserialize(resource).currency_codes

    @get_exception
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




