# from violas_client import Client, Wallet
# from violas_client.lbrtypes.account_config import treasury_compliance_account_address, association_address
from exchange_client import Client, Wallet
from lbrtypes.account_config import treasury_compliance_account_address, association_address
import time
from move_core_types.language_storage import core_code_address

# coins = ['Coin1', 'Coin2', 'LBR', 'VLSUSD', 'VLSEUR', 'VLSGBP', 'VLSSGD', 'VLS', 'USD', 'EUR', 'GBP', 'SGD', 'BTC']
client = Client("violas_testnet")
client.set_exchange_module_address(core_code_address())
client.set_exchange_owner_address(association_address())
wallet = Wallet.new()
a1 = wallet.new_account()
a2 = wallet.new_account()
seq = client.mint_coin(a1.address, 10_000_000, auth_key_prefix=a1.auth_key_prefix, is_blocking=True, currency_code="VLSUSD")
client.add_currency_to_account(a1, "VLSEUR")
seq = client.swap(a1, "VLSUSD", "VLSEUR", 100)
print(client.get_account_transaction(a1.address, seq, True).get_code_type())
# seq = client.mint_coin(a2.address, 10_000_000, auth_key_prefix=a2.auth_key_prefix, is_blocking=True, currency_code="VLSUSD")

# print(client.swap_get_swap_output_amount("VLSUSD", "VLSEUR", 1000))
# print(client.swap_get_reserves_resource())
# print(client.get_account_state(association_address()).swap_get_registered_currencies(core_code_address()))
# print(client.get_registered_currencies())
# wallet = Wallet.new()
# a1 = wallet.new_account()
# a2 = wallet.new_account()
# seq = client.mint_coin(a1.address, 10_000_000, auth_key_prefix=a1.auth_key_prefix, is_blocking=True, currency_code="Coin1")
# seq = client.mint_coin(a2.address, 10_000_000, auth_key_prefix=a2.auth_key_prefix, is_blocking=True, currency_code="Coin1")
# seq = client.transfer_coin(a2, a1.address, 100, gas_unit_price=2, currency_code="Coin1")
# print(client.get_account_transaction(a2.address, seq).get_gas_used_price())


