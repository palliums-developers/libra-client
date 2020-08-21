from bank_client import Client, Wallet
from move_core_types.language_storage import core_code_address
import time

client = Client("bj_testnet")
client.set_bank_owner_address("da13aace1aa1c49e497416a9dd062ecb")
client.set_bank_module_address(core_code_address())

data = "data"
data_hex = b"data".hex()
wallet = Wallet.new()
module_account = wallet.new_account()
client.mint_coin(module_account.address, 200_000_000, auth_key_prefix=module_account.auth_key_prefix,
                 currency_code="USD")
seq = client.bank_publish(module_account, data=data)
assert client.get_account_transaction(module_account.address, seq).get_data() == data_hex

a1 = wallet.new_account()
client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="USD")
seq = client.bank_publish(a1, data=data)
assert client.get_account_transaction(a1.address, seq).get_data() == data_hex

seq = client.bank_lock(a1, 100_000_000, currency_code="USD", data=data)
assert client.get_account_transaction(a1.address, seq).get_data() == data_hex