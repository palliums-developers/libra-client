from violas_client import Client, Wallet
from violas_client.move_core_types.language_storage import core_code_address

client = Client("libra_testnet")
tx = client.get_transaction(625063)
print(tx)

# wallet = Wallet.new()
# module_account = wallet.new_account()
# client.mint_coin(module_account.address, 200_000_000, auth_key_prefix=module_account.auth_key_prefix,
#                  currency_code="USD")
# seq = client.bank_publish(module_account)
# client.get_account_transaction(module_account.address, seq).get_amount()