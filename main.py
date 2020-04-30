from libra_client import Client
from libra.account_config import AccountConfig
from canoser import StrT
address = AccountConfig.association_address()
from libra_client import Wallet
from libra.transaction import Script, TransactionPayload, SignedTransaction
from json_rpc.views import EventView, TransactionView
from test import create_accounts, create_client, create_accounts_with_coins

# [a1] = create_accounts(1)
# client = create_client()
# client.mint_coin(a1.address, 100, receiver_auth_key_prefix_opt=a1.auth_key_prefix, is_blocking=True)
# assert 100 == client.get_balance(a1.address)

# assert 0

