from typing import Optional
from libra_client import Client as LibraClient
from extypes.transaction.module import Module
from extypes.transaction.script import Script
from lbrtypes.transaction.transaction_argument import TransactionArgument
from extypes.bytecode import CodeType
from extypes.account_state import AccountState

class Client(LibraClient):

    DEAD_LINE = 7258089600

    def publish_exchange(self, sender_account, is_blocking=True, **kwargs):
        module = Module.gen_module(sender_account.address)
        return self.submit_module(sender_account, module, is_blocking, **kwargs)

    def add_liquidity(self, sender_account, min_liquidity, max_token_amount, violas_amount, token_name, token_module_address=None, exchange_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(min_liquidity))
        args.append(TransactionArgument.to_U64(max_token_amount))
        args.append(TransactionArgument.to_U64(violas_amount))
        args.append(TransactionArgument.to_U64(self.DEAD_LINE))

        ty_args = self.get_type_args(token_module_address, token_name)
        script = Script.gen_script(CodeType.ADD_LIQUIDITY, *args, ty_args=ty_args, module_address=self.get_exchange_module_address(exchange_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def initialize(self, sender_account, exchange_module_address=None, is_blocking=True, **kwargs):
        args = []
        script = Script.gen_script(CodeType.INITIALIZE, *args, module_address=self.get_exchange_module_address(exchange_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def publish_reserve(self, sender_account, token_name, token_module_address=None, exchange_module_address=None, is_blocking=True, **kwargs):
        args = []

        ty_args = self.get_type_args(token_module_address, token_name)
        script = Script.gen_script(CodeType.PUBLISH_RESERVER, *args, ty_args=ty_args, module_address=self.get_exchange_module_address(exchange_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def remove_liquidity(self, sender_account, amount, min_violas, min_tokens, token_name, token_module_address=None, exchange_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))
        args.append(TransactionArgument.to_U64(min_violas))
        args.append(TransactionArgument.to_U64(min_tokens))
        args.append(TransactionArgument.to_U64(self.DEAD_LINE))

        ty_args = self.get_type_args(token_module_address, token_name)
        script = Script.gen_script(CodeType.REMOVE_LIQUIDITY, *args, ty_args=ty_args, module_address=self.get_exchange_module_address(exchange_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def token_to_token_swap(self, sender_account, tokens_sold, min_tokens_bought, min_violas_bought,
             sold_token_name, bought_token_name, sold_token_module_address=None, bought_token_module_address=None,exchange_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(tokens_sold))
        args.append(TransactionArgument.to_U64(min_tokens_bought))
        args.append(TransactionArgument.to_U64(min_violas_bought))
        args.append(TransactionArgument.to_U64(self.DEAD_LINE))

        token_types = self.get_type_args(sold_token_module_address, sold_token_name)
        bought_token_type = self.get_type_args(bought_token_module_address, bought_token_name)
        token_types.extend(bought_token_type)
        script = Script.gen_script(CodeType.TOKEN_TO_TOKEN_SWAP, *args, ty_args=token_types, module_address=self.get_exchange_module_address(exchange_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def token_to_violas_swap(self, sender_account, tokens_sold, min_violas, token_name, token_module_address=None, exchange_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(tokens_sold))
        args.append(TransactionArgument.to_U64(min_violas))
        args.append(TransactionArgument.to_U64(self.DEAD_LINE))

        ty_args = self.get_type_args(token_module_address, token_name)
        script = Script.gen_script(CodeType.TOKEN_TO_VIOLAS_SWAP, *args, ty_args=ty_args, module_address=self.get_exchange_module_address(exchange_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def violas_to_token_swap(self, sender_account, violas_sold, min_tokens, token_name, token_module_address=None, exchange_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(violas_sold))
        args.append(TransactionArgument.to_U64(min_tokens))
        args.append(TransactionArgument.to_U64(self.DEAD_LINE))

        ty_args = self.get_type_args(token_module_address, token_name)

        script = Script.gen_script(CodeType.VIOLAS_TO_TOKEN_SWAP, *args, ty_args=ty_args, module_address=self.get_exchange_module_address(exchange_module_address))

        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def get_exchange_module_address(self, exchange_module_address=None):
        if exchange_module_address:
            return exchange_module_address
        if hasattr(self, "exchange_module_address"):
            return self.exchange_module_address

    def set_exchange_module_addres(self, exchange_module_address):
        self.exchange_module_address = exchange_module_address

    def get_account_blob(self, account_address) -> Optional[AccountState]:
        blob = super().get_account_blob(account_address)
        if blob:
            state = AccountState.new(blob)
            state.set_exchange_module_address(self.get_exchange_module_address())
            return state

    def get_account_state(self, account_address) -> Optional[AccountState]:
        blob = super().get_account_blob(account_address)
        if blob:
            state = AccountState.new(blob)
            state.set_exchange_module_address(self.get_exchange_module_address())
            return state
    
    def get_liquidity_balance(self, liquidity_address, token_name, token_module_address=None, exchange_module_address=None):
        state = self.get_account_state(self.get_exchange_module_address(exchange_module_address))
        if state:
            reserve_resource = state.get_reserve_resource(token_name, token_module_address)
            if reserve_resource:
                token_reserve = reserve_resource.get_token_amount()
                violas_reserve = reserve_resource.get_violas_amount()
                total_liquidity = reserve_resource.get_liquidity_total_supply()
                state = self.get_account_state(liquidity_address)
                if state:
                    liquidity_resource = state.get_exchange_resource(token_name, exchange_module_address, token_module_address)
                    if liquidity_resource:
                        liquidity_amount = liquidity_resource.get_amount()
                        if total_liquidity == 0:
                            return 0, 0 ,0
                        violas_amount = liquidity_amount* violas_reserve / total_liquidity
                        token_amount = liquidity_amount* token_reserve/ total_liquidity
                        return liquidity_amount, violas_amount, token_amount

    def get_registered_currencies(self, exchange_module_address=None):
        state = self.get_account_state(self.get_exchange_module_address(exchange_module_address))
        if state:
            return state.get_registered_currencies().currency_codes


    def get_liquidity_balances(self, liquidity_address, exchange_module_address=None):
        exchange_state = self.get_account_state(self.get_exchange_module_address(exchange_module_address))
        if exchange_state and exchange_state.is_contract_address():
            currencies = exchange_state.get_registered_currencies()
            if currencies:
                ret = {}
                liquidity_state = self.get_account_state(liquidity_address)
                if liquidity_state:
                    for currency in currencies:
                        reserve_resource = exchange_state.get_reserve_resource(currency)
                        token_reserve = reserve_resource.get_token_amount()
                        violas_reserve = reserve_resource.get_violas_amount()
                        total_liquidity = reserve_resource.get_liquidity_total_supply()
                        ret[currency] = liquidity_state.get_liquidity_balance(token_reserve, violas_reserve, total_liquidity, currency, exchange_module_address=self.get_exchange_module_address(exchange_module_address))
                    return ret




