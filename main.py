from bank_client import Client
from bank_client.wallet_library import Wallet

client = Client()
wallet = Wallet.new()
module_account = wallet.new_account()
l_account = wallet.new_account()
client.mint_coin(module_account.address, 100_000_000, auth_key_prefix=module_account.auth_key_prefix)
client.bank_publish_contract(module_account)
client.bank_publish(module_account, bank_module_address=module_account.address)



