# from violas_client import Client, Wallet
# from violas_client.lbrtypes.account_config import treasury_compliance_account_address, association_address
from exchange_client import Client, Wallet
from lbrtypes.account_config import treasury_compliance_account_address, association_address
import time
from move_core_types.language_storage import core_code_address

print(core_code_address().hex())

wallet = Wallet.new()
client = Client("violas_testnet")
print(client.get_balances("0000000000000000000000000a550c18"))
# module_account = wallet.new_account()
# client.mint_coin(module_account.address, 10_000_000, auth_key_prefix=module_account.auth_key_prefix, is_blocking=True)
# client.swap_publish_contract(module_account)
# client.set_exchange_module_address(module_account.address)
# seq = client.swap_initialize(module_account)
# tx = client.get_account_transaction(module_account.address, seq)
# print(tx.get_code_type())
# resource = client.get_account_state(module_account.address).swap_get_reserves_resource()
# assert resource is not None