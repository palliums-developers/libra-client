from bank_client import Wallet, Client
from move_core_types.language_storage import core_code_address


module_address = "da13aace1aa1c49e497416a9dd062ecb"

client = Client()
client.set_bank_module_address(core_code_address())
client.set_bank_owner_address(module_address)

wallet = Wallet.new()
a1 = wallet.new_account()
client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="USD")
client.bank_publish(a1)
client.bank_lock(a1, 200_000_000, currency_code="USD")
client.bank_borrow(a1, 10_000_000, currency_code="USD")
_, amount = client.bank_get_borrow_amount(a1.address, "USD")
# client.bank_repay_borrow(a1, currency_code="USD", amount=amount)
# assert client.bank_get_borrow_amount(a1.address, currency_code="USD")[0] == 0