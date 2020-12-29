from violas_client import Client, Wallet
import time
from enum import IntEnum
from violas_client.extypes.bytecode import CodeType as ExchangeType

import time
client = Client("violas_testnet")
tx = client.get_transaction(1021354)
print(tx)
# value = client.swap_get_reward_balance("e58e356451edb15e3a4b26129cd1ba69")
# print(value)

# wallet = Wallet.new()
#
# liquidity_account = wallet.new_account()
# client.add_currency_to_account(liquidity_account, "EUR")
# client.mint_coin(liquidity_account.address, 10_000_000, currency_code="EUR",
#                  auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)
# client.add_currency_to_account(liquidity_account, "GBP")
# client.mint_coin(liquidity_account.address, 10_000_000, currency_code="GBP",
#                  auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)
#
# client.swap_add_liquidity(liquidity_account, "GBP", "EUR", 200_000, 100_000)
# time.sleep(1)
# amount = client.swap_get_reward_balance(liquidity_account.address_hex)