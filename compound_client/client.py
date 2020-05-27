from libra_client import Client as LibraClient
from cmpdtypes.transaction.module import Module
from cmpdtypes.transaction.script import Script
from cmpdtypes.bytecode import CodeType
from cmpdtypes.account_state import AccountState
from lbrtypes.transaction.transaction_argument import TransactionArgument
from typing import Optional

class Client(LibraClient):

    def compound_publish_bank(self, sender_account, is_blocking=True, **kwargs):
        module = Module.gen_module(sender_account.address)
        return self.submit_module(sender_account, module, is_blocking, **kwargs)

    def compound_borrow(self, sender_account, amount, data=None, token_name=None, token_module_address=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        ty_args = self.get_type_args(token_module_address, token_name)
        script = Script.gen_script(CodeType.BORROW, *args, ty_args=ty_args, module_address=self.get_bank_module_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def compound_enter_bank(self, sender_account, amount, token_name=None, token_module_address=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))

        ty_args = self.get_type_args(token_module_address, token_name)
        script = Script.gen_script(CodeType.ENTER_BANK, *args, ty_args=ty_args, module_address=self.get_bank_module_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def compound_exit_bank(self, sender_account, amount, token_module_address=None, token_name=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))

        ty_args = self.get_type_args(token_module_address, token_name)
        script = Script.gen_script(CodeType.EXIT_BANK, *args, ty_args=ty_args, module_address=self.get_bank_module_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def compound_liquidate_borrow(self, sender_account, borrower, amount, data=None, token_name=None, token_module_address=None, collateral_module_address=None, collateral_module_name=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_address(borrower, hex=False))
        args.append(TransactionArgument.to_U64(amount))
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        ty_args = self.get_type_args(token_module_address, token_name)
        ty_args.extend(self.get_type_args(bank_module_address, collateral_module_address, collateral_module_name))
        script = Script.gen_script(CodeType.LIQUIDATE_BORROW, *args, ty_args=ty_args, module_address=self.get_bank_module_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def compound_lock(self, sender_account, amount, data=None, token_name=None, token_module_address=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        ty_args = self.get_type_args(token_module_address, token_name)
        script = Script.gen_script(CodeType.LOCK, *args, ty_args=ty_args, module_address=self.get_bank_module_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def compound_publish(self, sender_account, data=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        script = Script.gen_script(CodeType.PUBLISH, *args, ty_args=[], module_address=self.get_bank_module_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def compound_redeem(self, sender_account, amount, data=None, token_name=None, token_module_address=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        ty_args = self.get_type_args(token_module_address, token_name)
        script = Script.gen_script(CodeType.REDEEM, *args, ty_args=ty_args, module_address=self.get_bank_module_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def compound_register_token(self, bank_module_account, price_oracle, collateral_factor, tokendata=None, token_name=None, token_module_address=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        collateral_factor = int(collateral_factor * (2**32))
        args.append(TransactionArgument.to_address(price_oracle))
        args.append(TransactionArgument.to_U64(collateral_factor))
        args.append(TransactionArgument.to_U8Vector(tokendata))

        ty_args = self.get_type_args(token_module_address, token_name)
        script = Script.gen_script(CodeType.REGISTER_TOKEN, *args, ty_args=ty_args, module_address=self.get_bank_module_address(bank_module_address))
        return self.submit_script(bank_module_account, script, is_blocking, **kwargs)

    def compound_repay_borrow(self, sender_account, amount, data=None, token_name=None, token_module_address=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        ty_args = self.get_type_args(token_module_address, token_name)
        script = Script.gen_script(CodeType.REPAY_BORROW, *args, ty_args=ty_args, module_address=self.get_bank_module_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def compound_update_collateral_factor(self, sender_account, factor, token_name=None, token_module_address=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(factor))

        ty_args = self.get_type_args(token_module_address, token_name)
        script = Script.gen_script(CodeType.UPDATE_COLLATERAL_FACTOR, *args, ty_args=ty_args, module_address=self.get_bank_module_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def compound_update_price(self, sender_account, price, token_name=None, token_module_address=None, bank_module_address=None, is_blocking=True, **kwargs):
        price = int(price*2**32)
        args = []
        args.append(TransactionArgument.to_U64(price))

        ty_args = self.get_type_args(token_module_address, token_name)
        script = Script.gen_script(CodeType.UPDATE_PRICE, *args, ty_args=ty_args, module_address=self.get_bank_module_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def get_account_blob(self, account_address) -> Optional[AccountState]:
        blob = super().get_account_blob(account_address)
        if blob:
            state = AccountState.new(blob)
            state.set_bank_module_address(self.get_bank_module_address())
            return state

    def get_account_state(self, account_address) -> Optional[AccountState]:
        blob = super().get_account_blob(account_address)
        if blob:
            state = AccountState.new(blob)
            state.set_bank_module_address(self.get_bank_module_address())
            return state

    def get_deposit_amount(self, account_address, token_name=None, token_module_address=None, bank_module_address=None):
        bank_module_address = self.get_bank_module_address(bank_module_address)
        state = self.get_account_state(bank_module_address)
        if state:
            exchange_rate = state.get_exchange_rate(token_name, token_module_address)
            index = state.get_token_index(token_name, token_module_address)
            state = self.get_account_state(account_address)
            if state:
                return state.get_deposit_amount(index, exchange_rate)
    
    def get_borrow_amount(self, account_address, token_name, token_module_address=None, bank_module_address=None):
        bank_module_address = self.get_bank_module_address(bank_module_address)
        state = self.get_account_state(bank_module_address)
        if state:
            borrow_index = state.get_borrow_index(token_name, token_module_address)
            index = state.get_token_index(token_name, token_module_address)
            state = self.get_account_state(account_address)
            if state:
                return state.get_borrow_amount(index, borrow_index)

    def set_bank_module_address(self, address):
        self.bank_module_address = address

    def get_bank_module_address(self, address=None):
        if address:
            return address
        if hasattr(self, "bank_module_address"):
            return self.bank_module_address
