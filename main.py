import random
import time
from libra_client import Client, Wallet

from violas_client import Wallet, Client
from violas_client.move_core_types.language_storage import core_code_address

module_address = "00000000000000000000000045584348"
# module_address = "241dfc7d468f18d43e894675939e6057"

# client = Client("violas_testnet")
client = Client("bj_testnet")
# ac = client.get_account_state(client.EXCHANGE_OWNER_ADDRESS)
# print(ac.swap_get_tokens_resource())
print(client.swap_get_registered_currencies())

# client.set_exchange_module_address(core_code_address())
# client.set_exchange_owner_address(module_address)
#
# wallet = Wallet.new()
# acc_a = wallet.new_account()
# acc_b = wallet.new_account()
# addr_a = acc_a.address_hex
# addr_b = acc_b.address_hex
# print(addr_a, " | ", addr_b)
#
#
# client.mint_coin(acc_a.address, 10_000_000, auth_key_prefix=acc_a.auth_key_prefix, is_blocking=True,
#                  currency_code="VUSDT")
# client.add_currency_to_account(acc_a, "VBTC")
# client.add_currency_to_account(acc_a, "VLS")
# client.mint_coin(acc_a.address, 10_000_000, auth_key_prefix=acc_a.auth_key_prefix, is_blocking=True,
#                  currency_code="VBTC")
#
# amount_a0 = client.get_balance(acc_a.address, "VUSDT")
# amount_a1 = client.get_balance(acc_a.address, "VBTC")
# print("balances0: VUSDT,VBTC: ", amount_a0, amount_a1)
# client.swap_add_liquidity(acc_a, "VUSDT", "VBTC", 1_000_000, 321_432)