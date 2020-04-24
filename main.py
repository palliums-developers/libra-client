from libra_client import Client
from libra.account_config import AccountConfig
from canoser import StrT
address = AccountConfig.association_address()
from libra_client import Wallet
from libra.transaction import Script, TransactionPayload, SignedTransaction
from json_rpc.views import EventView, TransactionView
from test import create_accounts, create_client, create_accounts_with_coins

client = create_client()
[a1, a2] = create_accounts_with_coins(2)
[a3] = create_accounts(1)
seq = client.transfer_coin(a1, 10, a2.address, is_blocking=True, data="data")
print(client.get_balance(a3.address))
print(client.get_account_transaction(a1.address, seq, True))



