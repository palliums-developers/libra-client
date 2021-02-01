import random
import time
from violas_client import Client, Wallet
from violas_client.lbrtypes.bytecode import CodeType

start = 0
client = Client("bj_testnet")
while True:
    tx = client.get_transaction(start)
    if tx.get_code_type() == CodeType.UNKNOWN:
        print(start)
    start += 1

# client.mint_coin("b14bc3286e4b9b41c86022f2e614d721", 99, currency_code="vBTC")


# wallet = Wallet.new()
#
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

