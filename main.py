import random
import time
from violas_client import Client, Wallet


client = Client("violas_testnet")
wallet = Wallet.new()
client = Client()
liquidity_account = wallet.new_account()
client.mint_coin(liquidity_account.address, 10_000_000, currency_code="vBTC",
                 auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)
client.add_currency_to_account(liquidity_account, "vUSDT")

client.mint_coin(liquidity_account.address, 10_000_000, currency_code="vUSDT",
                 auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)
client.add_currency_to_account(liquidity_account, "VLS")

client.swap_add_liquidity(liquidity_account, "vBTC", "vUSDT", 200_000, 100_000)
time.sleep(1)
amount = client.swap_get_reward_balance(liquidity_account.address_hex)