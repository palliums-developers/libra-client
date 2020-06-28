from libra_client import Client as LibraClient
from banktypes.transaction.module import Module
from banktypes.transaction.script import Script
from banktypes.bytecode import CodeType
from banktypes.account_state import AccountState
from lbrtypes.transaction.transaction_argument import TransactionArgument
from typing import Optional

class Client(LibraClient):

    def bank_release_contract(self, sender_account, is_blocking=True, **kwargs):
        module = Module.gen_module(sender_account.address)
        return self.submit_module(sender_account, module, is_blocking, **kwargs)

    def bank_borrow(self, sender_account, amount, data=None, currency_code=None, currency_module_address=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        ty_args = self.get_type_args(currency_module_address, currency_code)
        script = Script.gen_script(CodeType.BORROW, *args, ty_args=ty_args, module_address=self.bank_get_contract_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def bank_enter(self, sender_account, amount, currency_code=None, currency_module_address=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))

        ty_args = self.get_type_args(currency_module_address, currency_code)
        script = Script.gen_script(CodeType.ENTER_BANK, *args, ty_args=ty_args, module_address=self.bank_get_contract_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def bank_exit(self, sender_account, amount, currency_module_address=None, currency_code=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))

        ty_args = self.get_type_args(currency_module_address, currency_code)
        script = Script.gen_script(CodeType.EXIT_BANK, *args, ty_args=ty_args, module_address=self.bank_get_contract_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def bank_liquidate_borrow(self, sender_account, borrower, amount, data=None, currency_code=None, currency_module_address=None, collateral_module_address=None, collateral_module_name=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_address(borrower, hex=False))
        args.append(TransactionArgument.to_U64(amount))
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        ty_args = self.get_type_args(currency_module_address, currency_code)
        ty_args.extend(self.get_type_args(bank_module_address, collateral_module_address, collateral_module_name))
        script = Script.gen_script(CodeType.LIQUIDATE_BORROW, *args, ty_args=ty_args, module_address=self.bank_get_contract_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def bank_lock(self, sender_account, amount, data=None, currency_code=None, currency_module_address=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        ty_args = self.get_type_args(currency_module_address, currency_code)
        script = Script.gen_script(CodeType.LOCK, *args, ty_args=ty_args, module_address=self.bank_get_contract_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def bank_publish(self, sender_account, data=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        script = Script.gen_script(CodeType.PUBLISH, *args, ty_args=[], module_address=self.bank_get_contract_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def bank_redeem(self, sender_account, amount=0, data=None, currency_code=None, currency_module_address=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        ty_args = self.get_type_args(currency_module_address, currency_code)
        script = Script.gen_script(CodeType.REDEEM, *args, ty_args=ty_args, module_address=self.bank_get_contract_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def bank_register_token(self, bank_module_account, price_oracle, collateral_factor, tokendata=None, currency_code=None, currency_module_address=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        collateral_factor = int(collateral_factor * (2**32))
        args.append(TransactionArgument.to_address(price_oracle))
        args.append(TransactionArgument.to_U64(collateral_factor))
        args.append(TransactionArgument.to_U8Vector(tokendata))

        ty_args = self.get_type_args(currency_module_address, currency_code)
        script = Script.gen_script(CodeType.REGISTER_TOKEN, *args, ty_args=ty_args, module_address=self.bank_get_contract_address(bank_module_address))
        return self.submit_script(bank_module_account, script, is_blocking, **kwargs)

    def bank_repay_borrow(self, sender_account, amount=0, data=None, currency_code=None, currency_module_address=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        ty_args = self.get_type_args(currency_module_address, currency_code)
        script = Script.gen_script(CodeType.REPAY_BORROW, *args, ty_args=ty_args, module_address=self.bank_get_contract_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def bank_update_collateral_factor(self, sender_account, factor, currency_code=None, currency_module_address=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(factor))

        ty_args = self.get_type_args(currency_module_address, currency_code)
        script = Script.gen_script(CodeType.UPDATE_COLLATERAL_FACTOR, *args, ty_args=ty_args, module_address=self.bank_get_contract_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def bank_update_price(self, sender_account, price, currency_code=None, currency_module_address=None, bank_module_address=None, is_blocking=True, **kwargs):
        price = int(price*2**32)
        args = []
        args.append(TransactionArgument.to_U64(price))

        ty_args = self.get_type_args(currency_module_address, currency_code)
        script = Script.gen_script(CodeType.UPDATE_PRICE, *args, ty_args=ty_args, module_address=self.bank_get_contract_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def bank_get_account_blob(self, account_address) -> Optional[AccountState]:
        blob = super().get_account_blob(account_address)
        state = AccountState.new(blob)
        state.set_bank_module_address(self.bank_get_contract_address())
        return state

    def bank_get_account_state(self, account_address) -> Optional[AccountState]:
        blob = super().get_account_blob(account_address)
        state = AccountState.new(blob)
        state.set_bank_module_address(self.bank_get_contract_address())
        return state

    def bank_get_bank_amount(self, account_address, currency_code=None, currency_module_address=None, bank_module_address=None):
        bank_module_address = self.bank_get_contract_address(bank_module_address)
        state = self.get_account_state(bank_module_address)
        index = state.get_token_index(currency_code, currency_module_address)
        state = self.get_account_state(account_address)
        return state.get_bank_amount(index, bank_module_address)

    def bank_get_lock_amount(self, account_address, currency_code=None, currency_module_address=None, bank_module_address=None):
        bank_module_address = self.bank_get_contract_address(bank_module_address)
        state = self.get_account_state(bank_module_address)
        exchange_rate = state.get_exchange_rate(currency_code, currency_module_address)
        index = state.get_token_index(currency_code, currency_module_address)
        state = self.get_account_state(account_address)
        return state.get_lock_amount(index, exchange_rate, self.bank_get_contract_address(bank_module_address))

    def bank_get_cur_lock_rate(self, currency_code=None, currency_module_address=None, bank_module_address=None):
        bank_module_address = self.bank_get_contract_address(bank_module_address)
        state = self.get_account_state(bank_module_address)
        return state.get_cur_lock_rate(currency_code, currency_module_address)

    def bank_get_borrow_amount(self, account_address, currency_code=None, currency_module_address=None, bank_module_address=None, include_interest=True):
        bank_module_address = self.bank_get_contract_address(bank_module_address)
        bank_module_address = self.bank_get_contract_address(bank_module_address)
        state = self.get_account_state(bank_module_address)
        index = state.get_token_index(currency_code, currency_module_address)
        _, _, cur_interest_index = state.get_cur_interest_index(index)
        state = self.get_account_state(account_address)
        return state.get_borrow_amount(index, cur_interest_index, bank_module_address, include_interest)

    def bank_get_cur_borrow_rate(self, currency_code=None, currency_module_address=None, bank_module_address=None):
        bank_module_address = self.bank_get_contract_address(bank_module_address)
        state = self.get_account_state(bank_module_address)
        return state.get_cur_borrow_rate(currency_code, currency_module_address)

    def bank_get_utilization(self, currency_code=None, currency_module_address=None, bank_module_address=None):
        bank_module_address = self.bank_get_contract_address(bank_module_address)
        state = self.get_account_state(bank_module_address)
        return state.get_cur_borrow_rate(currency_code, currency_module_address)

    def bank_set_contract_address(self, address):
        self.bank_module_address = address

    def bank_get_contract_address(self, address=None):
        if address:
            return address
        if hasattr(self, "bank_module_address"):
            return self.bank_module_address
