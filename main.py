from violas_client import Client, Wallet
from violas_client.move_core_types.language_storage import core_code_address
from violas_client.lbrtypes.account_config import association_address

bank_module_address = "da13aace1aa1c49e497416a9dd062ecb"
exchange_module_address = "00000000000000000000000045584348"

client = Client("violas_testnet")
client.set_bank_module_address(core_code_address())
client.set_bank_owner_address(bank_module_address)
client.set_exchange_module_address(core_code_address())
client.set_exchange_owner_address(exchange_module_address)

wallet = Wallet.new()
a1 = wallet.new_account()
client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix)
client.bank_publish(a1)
client.add_currency_to_account(a1, "USD")
client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="USD")
client.bank_lock(a1, 100_000_000, currency_code="USD")
print(client.get)
