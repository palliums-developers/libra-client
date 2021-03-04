import random
import time
from libra_client import Client, Wallet

code = "trouble menu nephew group alert recipe hotel fatigue wet shadow say fold huge olive solution enjoy garden appear vague joy great keep cactus melt"

<<<<<<< HEAD
client = Client("violas_testnet")
tx = client.get_transaction(19254391)
print(tx.get_code_type())
=======
wallet = Wallet.new()
client = Client.new("violas_testnet", chain_id=4)
w = wallet.new()
a = w.new_account()
client.mint_coin(a.address_hex, 100, a.auth_key_prefix)
# liquidity_account = w.new_account()
# a1 = w.new_account()
# print(client.swap_get_liquidity_balances(liquidity_account.address_hex))
# print(client.get_account_registered_currencies(liquidity_account.address_hex))
# client.add_currency_to_account(a1, "vUSDT")
# client.transfer_coin(liquidity_account, a1.address_hex, 10000, currency_code="vBTC")
# client.transfer_coin(liquidity_account, a1.address_hex, 10000, currency_code="vUSDT")

# client.add_currency_to_account(liquidity_account, "vUSDT")
# client.add_currency_to_account(liquidity_account, "VLS")
# client.mint_coin(liquidity_account.address, 10_000_000, currency_code="vUSDT",
#                  auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)
#
# client.swap_add_liquidity(liquidity_account, "vBTC", "vUSDT", 200_000, 100_000)
# values = client.swap_get_liquidity_balances(liquidity_account.address)[0]
# print(values["liquidity"])
# client.swap_remove_liquidity(liquidity_account, "vBTC", "vUSDT", 10000)
# while True:
#     tx = client.get_transaction(start)
#     if tx.get_code_type() == CodeType.UNKNOWN:
#         print(start)
#     start += 1
#
# client = Client()
# wallet = Wallet.new()
# a1 = wallet.new_account()
# client.mint_coin(a1.address, 100, auth_key_prefix=a1.auth_key_prefix, currency_code="vBTC")
# client.mint_coin(a1.address, 100, auth_key_prefix=a1.auth_key_prefix, currency_code="vBTC")
# client.mint_coin(a1.address, 100, auth_key_prefix=a1.auth_key_prefix, currency_code="vBTC")
>>>>>>> master
#
# #
# i = 0
# while True:
#     a1 = wallet.new_account()
#
#
#     btc_amount = random.randint(1_000, 1_000_000_000)
#     client.mint_coin(a1.address_hex, btc_amount, auth_key_prefix=a1.auth_key_prefix, currency_code="vBTC")
#     client.add_currency_to_account(a1, "vUSDT")
#     usdt_amount = random.randint(1_000, 1_000_000_000_000)
#     client.mint_coin(a1.address_hex, usdt_amount, auth_key_prefix=a1.auth_key_prefix, currency_code="vUSDT")
#     client.bank_publish(a1)
#     client.bank_lock2(a1, btc_amount, "vBTC")
#     client.bank_lock2(a1, usdt_amount, "vUSDT")
#     client.bank_borrow2(a1, int(btc_amount/2)-10, "vBTC")
#     client.bank_borrow2(a1, int(usdt_amount/2)-10, "vUSDT")
#     time.sleep(1)
#     i += 1
#     print(i)

