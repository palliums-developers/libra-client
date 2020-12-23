from violas_client import Client, Wallet
import time
from enum import IntEnum

wallet = Wallet.new()
client = Client()
liquidity_account = wallet.new_account()
client.mint_coin(liquidity_account.address, 10_000_000, currency_code="USD",
                 auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)
client.add_currency_to_account(liquidity_account, "GBP")
client.add_currency_to_account(liquidity_account, "VLS")

client.mint_coin(liquidity_account.address, 10_000_000, currency_code="GBP",
                 auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)

client.swap_add_liquidity(liquidity_account, "GBP", "USD", 200_000, 100_000)
time.sleep(1)
amount = client.swap_get_reward_balance(liquidity_account.address_hex)
seq = client.swap_withdraw_mine_reward(liquidity_account)
tx = client.get_account_transaction(liquidity_account.address_hex, seq)
print(amount, tx.get_swap_reward_amount())

