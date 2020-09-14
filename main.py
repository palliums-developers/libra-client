from violas_client import Client, Wallet
from move_core_types.language_storage import core_code_address
from lbrtypes.account_config import association_address
import time





bank_module_address = "00000000000000000000000042414E4B"
exchange_module_address = "00000000000000000000000045584348"

client = Client()
client.set_bank_module_address(core_code_address())
client.set_bank_owner_address(bank_module_address)
# client.set_exchange_module_address(core_code_address())
# client.set_exchange_owner_address(exchange_module_address)

wallet = Wallet.new()
a1 = wallet.new_account()
a2 = wallet.new_account()
print(client.bank_get_amount(a1.address, "USD"))
# client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="USD")
# client.mint_coin(a2.address, 300_000_000, auth_key_prefix=a2.auth_key_prefix, currency_code="USD")
# client.bank_publish(a1)
# client.bank_publish(a2)
# client.bank_lock(a1, 100_000_000, currency_code="USD")
# client.bank_borrow(a1, 10_000_000, currency_code="USD")
# client.bank_lock(a2, 100_000_000, currency_code="USD")
# lock_rate = client.bank_get_lock_rate("USD")
# lock_amount = client.bank_get_lock_amount(a2.address, currency_code="USD")
# client.bank_redeem(a2, currency_code="USD", amount=0)
# # print(client.bank_get_lock_amount(a2.address, "USD"))
# # print(lock_amount)
# # time.sleep(60)
# # lock_amount = client.bank_get_lock_amount(a2.address, currency_code="USD")
# # print(lock_amount)
# # client.bank_redeem(a2, currency_code="USD", amount=lock_amount)
# # print(client.bank_get_lock_amount(a2.address, "USD"))
#
# return_when_error