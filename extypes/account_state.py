from typing import Optional
from lbrtypes.account_state import AccountState as LibraAccountState
from extypes.exchange_resource import ReservesResource, RegisteredCurrenciesResource, TokensResource
from extypes.exdep_resource import BalanceResource
from move_core_types.language_storage import StructTag, TypeTag
from error import get_exception

class AccountState(LibraAccountState):
    @classmethod
    def new(cls, account_state: LibraAccountState):
        ret = cls()
        ret.ordered_map = account_state.ordered_map
        return ret

    @get_exception
    def swap_get_balance(self, currency_code, exchange_module_address=None) -> Optional[BalanceResource]:
        type_tag = TypeTag("Struct", StructTag.new(currency_code))
        resource = self.get(BalanceResource.resource_path_for(type_tag, module_address=self.get_exchange_module_address(exchange_module_address)))
        return BalanceResource.deserialize(resource).value

    @get_exception
    def swap_get_reserves_resource(self) -> Optional[ReservesResource]:
        resource = self.get(ReservesResource.resource_path(module_address=self.get_account_address()))
        return ReservesResource.deserialize(resource).reserves

    @get_exception
    def swap_get_tokens_resource(self, exchange_module_address=None) -> Optional[TokensResource]:
        resource = self.get(TokensResource.resource_path(module_address=self.get_exchange_module_address(exchange_module_address)))
        return TokensResource.deserialize(resource)

    @get_exception
    def swap_get_registered_currencies(self, exchange_module_address=None) -> Optional[RegisteredCurrenciesResource]:
        resource = self.get(RegisteredCurrenciesResource.resource_path(module_address=self.get_exchange_module_address(exchange_module_address)))
        return RegisteredCurrenciesResource.deserialize(resource)

    # @get_exception
    # def get_exchange_info_resource(self) -> Optional[ExchangeInfoResource]:
    #     resource = self.get(ExchangeInfoResource.resource_path_for(module_address=self.get_account_address()))
    #     return ExchangeInfoResource.deserialize(resource)
    #
    # @get_exception
    # def get_liquidity_balance(self, token_reserve, violas_reserve, total_liquidity, currency_code, currency_module_address=None, exchange_module_address=None):
    #     liquidity_resource = self.get_exchange_resource(currency_code, exchange_module_address=exchange_module_address, currency_module_address=currency_module_address)
    #     liquidity_amount = liquidity_resource.get_amount()
    #     if total_liquidity == 0:
    #         return 0, 0, 0
    #     violas_amount = liquidity_amount * violas_reserve / total_liquidity
    #     token_amount = liquidity_amount * token_reserve / total_liquidity
    #     return liquidity_amount, violas_amount, token_amount
    #
    # @get_exception
    # def get_registered_currencies(self):
    #     resource = self.get(RegisteredCurrenciesResource.resource_path_for(module_address=self.get_account_address()))
    #     return RegisteredCurrenciesResource.deserialize(resource).currency_codes
    #
    # @get_exception
    # def is_contract_address(self):
    #     return self.get_registered_currencies() is not None
    #
    def set_exchange_module_address(self, address):
        if address:
            self.exchange_module_address = address

    def get_exchange_module_address(self, address=None):
        if address:
            return address
        if hasattr(self, "exchange_module_address"):
            return self.exchange_module_address




