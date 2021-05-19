# import random
# import time
# from libra_client import Client, Wallet
#
# from violas_client import Wallet, Client
# from violas_client.move_core_types.language_storage import core_code_address
#
# client = Client("bj_testnet")
# wallet = Wallet.new()
# liquidity_account = wallet.new_account()
# client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix,
#                  is_blocking=True, currency_code="vUSDT")
# client.add_currency_to_account(liquidity_account, "vBTC")
# client.mint_coin(liquidity_account.address, 10_000_000, currency_code="vBTC",
#                  auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)

# import math
# v = math.pow(1.0001, 887272)
# print(int(v))
# print(2**128)
# print(1461446703485210103287273052203988822378723970342 >> 32)
# print(4295128739)
# print(0xfff97272373d413259a46990580e213a >> 126)
# print(0xfffcb933bd6fad37aa2d162d1a594001 >> 127)
print(2 ** 160)
print(1461446703485210103287273052203988822378723970342)

