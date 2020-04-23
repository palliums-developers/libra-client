from libra_client import Client
from libra.account_config import AccountConfig
from canoser import StrT
address = AccountConfig.association_address()
from libra_client import Wallet
from libra.transaction import Script, TransactionPayload, SignedTransaction
from json_rpc.views import EventView, TransactionView
from test import create_accounts, create_client, create_accounts_with_coins

client = create_client()
[a1, a2] = create_accounts(2)
seq = client.mint_coin(a1.address, 100, receiver_auth_key_prefix_opt=a1.auth_key_prefix, is_blocking=True)
tx = client.get_account_transaction(AccountConfig.association_address(), seq-1)
assert tx.get_sender() == AccountConfig.association_address()

