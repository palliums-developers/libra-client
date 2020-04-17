from libra_client import Client
from libra.account_config import AccountConfig
from canoser import StrT
address = AccountConfig.association_address()
from libra_client import Wallet
from libra.transaction import Script, TransactionPayload, SignedTransaction
from json_rpc.views import EventView, TransactionView
from test import create_accounts, create_client, create_accounts_with_coins

file_name = "./recover"
wallet = Wallet.new()
a1 = wallet.new_account()
wallet.write_recovery(file_name)
wallet = Wallet.recover(file_name)
assert a1.address == wallet.accounts[0].address
a2 = wallet.get_account_by_address_or_refid(a1.address)
a3 = wallet.get_account_by_address_or_refid(0)
assert a2.address == a1.address
assert a3.address == a1.address
