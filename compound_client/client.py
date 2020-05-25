from libra_client import Client as LibraClient
from cmpdtypes.transaction.module import Module
from cmpdtypes.transaction.script import Script
from cmpdtypes.bytecode import CodeType
from cmpdtypes.account_state import AccountState
from lbrtypes.transaction.transaction_argument import TransactionArgument
from typing import Optional

class Client(LibraClient):

    def publish_bank(self, sender_account, is_blocking=True, **kwargs):
        module = Module.gen_module(sender_account.address)
        return self.submit_module(sender_account, module, is_blocking, **kwargs)

    def borrow(self, sender_account, amount, data=None, token_module_address=None, token_module_name=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        ty_args = self.get_type_args(token_module_address, token_module_name)
        script = Script.gen_script(CodeType.BORROW, *args, ty_args=ty_args, module_address=self.get_bank_module_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def enter_bank(self, sender_account, amount, token_module_address=None, token_module_name=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))

        ty_args = self.get_type_args(token_module_address, token_module_name)
        script = Script.gen_script(CodeType.ENTER_BANK, *args, ty_args=ty_args, module_address=self.get_bank_module_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def exit_bank(self, sender_account, amount, token_module_address=None, token_module_name=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))

        ty_args = self.get_type_args(token_module_address, token_module_name)
        script = Script.gen_script(CodeType.EXIT_BANK, *args, ty_args=ty_args, module_address=self.get_bank_module_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def liquidate_borrow(self, sender_account, borrower, amount, data=None, token_module_address=None, token_module_name=None,  collateral_module_address=None, collateral_module_name=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_address(borrower, hex=False))
        args.append(TransactionArgument.to_U64(amount))
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        ty_args = self.get_type_args(token_module_address, token_module_name)
        ty_args.extend(self.get_type_args(bank_module_address, collateral_module_address, collateral_module_name))
        script = Script.gen_script(CodeType.LIQUIDATE_BORROW, *args, ty_args=ty_args, module_address=self.get_bank_module_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def lock(self, sender_account, amount, data=None, token_module_address=None, token_module_name=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        ty_args = self.get_type_args(token_module_address, token_module_name)
        script = Script.gen_script(CodeType.LOCK, *args, ty_args=ty_args, module_address=self.get_bank_module_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def publish(self, sender_account, data=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        script = Script.gen_script(CodeType.PUBLISH, *args, ty_args=[], module_address=self.get_bank_module_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def redeem(self, sender_account, amount, data=None, token_module_address=None, token_module_name=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        ty_args = self.get_type_args(token_module_address, token_module_name)
        script = Script.gen_script(CodeType.REDEEM, *args, ty_args=ty_args, module_address=self.get_bank_module_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def register_token(self, bank_module_account, price_oracle, collateral_factor, tokendata=None, token_module_address=None, token_module_name=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        collateral_factor = int(collateral_factor * (2**32))
        args.append(TransactionArgument.to_address(price_oracle))
        args.append(TransactionArgument.to_U64(collateral_factor))
        args.append(TransactionArgument.to_U8Vector(tokendata))

        ty_args = self.get_type_args(token_module_address, token_module_name)
        script = Script.gen_script(CodeType.REGISTER_TOKEN, *args, ty_args=ty_args, module_address=self.get_bank_module_address(bank_module_address))
        return self.submit_script(bank_module_account, script, is_blocking, **kwargs)

    def repay_borrow(self, sender_account, amount, data=None, token_module_address=None, token_module_name=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        ty_args = self.get_type_args(token_module_address, token_module_name)
        script = Script.gen_script(CodeType.REPAY_BORROW, *args, ty_args=ty_args, module_address=self.get_bank_module_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def update_collateral_factor(self, sender_account, factor, token_module_address=None, token_module_name=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(factor))

        ty_args = self.get_type_args(token_module_address, token_module_name)
        script = Script.gen_script(CodeType.UPDATE_COLLATERAL_FACTOR, *args, ty_args=ty_args, module_address=self.get_bank_module_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def update_price(self, sender_account, price, token_module_address=None, token_module_name=None, bank_module_address=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(price))

        ty_args = self.get_type_args(token_module_address, token_module_name)
        script = Script.gen_script(CodeType.UPDATE_PRICE, *args, ty_args=ty_args, module_address=self.get_bank_module_address(bank_module_address))
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

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

    def set_bank_module_address(self, address):
        self.bank_module_address = address

    def get_bank_module_address(self, address=None):
        if address:
            return address
        if hasattr(self, "bank_module_address"):
            return self.bank_module_address
