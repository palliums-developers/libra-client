from libra_client import Client
from libra.account_config import AccountConfig
from canoser import StrT
address = AccountConfig.association_address()
from libra_client import Wallet
from libra.transaction import Script, TransactionPayload, SignedTransaction
from json_rpc.views import EventView, TransactionView
from test import create_accounts, create_client, create_accounts_with_coins

from violas import Client as ViolasClient
from violas.error.error import LibraError

from libra_client import Client as LibraClient
from libra_client.error.error import LibraError as LibraError

# [a1] = create_accounts(1)
# client = create_client()
# balance = client.get_balance(a1.address)
# assert balance == 0
#
# client.mint_coin(a1.address, 100, receiver_auth_key_prefix_opt=a1.auth_key_prefix, is_blocking=True)
# balance = client.get_balance(a1.address)
# assert balance == 100