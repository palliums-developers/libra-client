# from violas_client import Client, Wallet
# from violas_client.lbrtypes.account_config import treasury_compliance_account_address, association_address
from exchange_client import Client, Wallet
from lbrtypes.account_config import treasury_compliance_account_address, association_address
import time
wallet = Wallet.new()
client = Client("violas_testnet")
print(client.get_transaction(1))
# module_account = wallet.new_account()
# client.mint_coin(module_account.address, 10_000_000, auth_key_prefix=module_account.auth_key_prefix, is_blocking=True)
# client.swap_publish_contract(module_account)
# # client.set_exchange_module_address(module_account.address)
# print(client.get_sequence_number(module_account.address))
#
# client.swap_initialize(module_account, is_blocking=False)
# time.sleep(1)
# print(client.get_sequence_number(module_account.address))
