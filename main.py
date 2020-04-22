from libra_client import Client
from libra.account_config import AccountConfig
from canoser import StrT
address = AccountConfig.association_address()
from libra_client import Wallet
from libra.transaction import Script, TransactionPayload, SignedTransaction
from json_rpc.views import EventView, TransactionView
from test import create_accounts, create_client, create_accounts_with_coins

a1, a2 = create_accounts_with_coins(2)
client = create_client()
tx = client.get_account_transaction(a1.address, 0, True)
assert tx is None
tx = client.get_account_transaction(AccountConfig.association_address(), 1, True)
assert isinstance(tx, TransactionView)

