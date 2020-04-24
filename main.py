from libra_client import Client
from libra.account_config import AccountConfig
from canoser import StrT
address = AccountConfig.association_address()
from libra_client import Wallet
from libra.transaction import Script, TransactionPayload, SignedTransaction
from json_rpc.views import EventView, TransactionView
from test import create_accounts, create_client, create_accounts_with_coins

from error import ViolasError
from error.status_code import StatusCode, ServerCode


a1, a2 = create_accounts(2)
client = create_client()

try:
    client.transfer_coin(a1, 100, a2.address, is_blocking=True)
    assert 0
except ViolasError as e:
    pass
client.mint_coin(a1.address, 100, receiver_auth_key_prefix_opt=a1.auth_key_prefix, is_blocking=True)

client.transfer_coin(a1, 10, a2.address, is_blocking=True)



