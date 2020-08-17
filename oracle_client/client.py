from typing import Union, Optional
from libra_client import Client as LibraClient
from lbrtypes.transaction.transaction_argument import TransactionArgument
from oracle_client.bytecodes import gen_script, CodeType
from oracle_client.account_state import AccountState

class Client(LibraClient):
    def update_exchange_rate(self, currency_code, numerator, denominator, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(numerator))
        args.append(TransactionArgument.to_U64(denominator))

        ty_args = self.get_type_args(currency_code)
        script = gen_script(CodeType.UPDATE_EXCHANGE_RATE, *args, ty_args=ty_args)
        return self.submit_script(self.associate_account, script, is_blocking, **kwargs)

    def get_account_state(self, account_address: Union[bytes, str]) -> Optional[AccountState]:
        blob = super().get_account_blob(account_address)
        if blob:
            state = AccountState.new(blob)
            if hasattr(self, "exchange_module_address"):
                state.set_exchange_module_address(self.exchange_module_address)
            return state

