# from violas_client import Client, Wallet
# from violas_client.lbrtypes.account_config import treasury_compliance_account_address, association_address
from exchange_client import Client, Wallet
from lbrtypes.account_config import treasury_compliance_account_address, association_address

wallet = Wallet.new()
client = Client()
module_account = wallet.new_account()
client.mint_coin(module_account.address, 10_000_000, auth_key_prefix=module_account.auth_key_prefix, is_blocking=True)
client.swap_publish_contract(module_account)
client.set_exchange_module_address(module_account.address)
client.swap_initialize(module_account)
client.swap_add_currency(module_account, "LBR")
client.swap_add_currency(module_account, "Coin1")
client.swap_add_currency(module_account, "Coin2")

liquidity_account = wallet.new_account()
client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix,
                 is_blocking=True)
client.add_currency_to_account(liquidity_account, "Coin1")
client.mint_coin(liquidity_account.address, 10_000_000, currency_code="Coin1",
                 auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)
client.add_currency_to_account(liquidity_account, "Coin2")
client.mint_coin(liquidity_account.address, 10_000_000, currency_code="Coin2",
                 auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)

swap_account = wallet.new_account()
client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix, is_blocking=True)
client.add_currency_to_account(swap_account, "Coin1")
client.mint_coin(swap_account.address, 10_000_000, currency_code="Coin1", auth_key_prefix=swap_account.auth_key_prefix,
                 is_blocking=True)
client.add_currency_to_account(swap_account, "Coin2")
client.mint_coin(swap_account.address, 10_000_000, currency_code="Coin2", auth_key_prefix=swap_account.auth_key_prefix,
                 is_blocking=True)

client.swap_add_liquidity(liquidity_account, "LBR", "Coin1", 123_321, 321_432)
client.swap_add_liquidity(liquidity_account, "Coin2", "Coin1", 321_432, 321_432)

value, fee= client.swap_get_swap_output_amount("Coin1", "LBR", 1000)
print(value, fee)
# wallet = Wallet.new()
# client = Client()
# print(client.get_transaction(15074))
# a1 = wallet.new_account()
# client.create_designated_dealer(a1.address, a1.auth_key_prefix, currency_code="Coin1")
# client.mint_coin(a1.address, 100000, currency_code="Coin1")
# client.preburn(a1, 100, "Coin1")
# print(client.get_balances(a1.address))
# # client.burn(a1.address, "Coin1", gas_currency_code="LBR")
# client.cancel_burn(a1.address, "Coin1", gas_currency_code="LBR")
# print(client.get_balances(a1.address))
# print(client.get_transaction(15100))
# client.swap_publish_contract(module_account)
# client.set_exchange_module_address(module_account.address)
# client.swap_initialize(module_account)
# client.swap_add_currency(module_account, "LBR")
# client.swap_add_currency(module_account, "Coin1")
# client.swap_add_currency(module_account, "Coin2")
#
# liquidity_account = wallet.new_account()
# client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix,
#                  is_blocking=True)
# client.add_currency_to_account(liquidity_account, "Coin1")
# client.mint_coin(liquidity_account.address, 10_000_000, currency_code="Coin1",
#                  auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)
# client.add_currency_to_account(liquidity_account, "Coin2")
# client.mint_coin(liquidity_account.address, 10_000_000, currency_code="Coin2",
#                  auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)
#
# swap_account = wallet.new_account()
# client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix, is_blocking=True)
# client.add_currency_to_account(swap_account, "Coin1")
# client.mint_coin(swap_account.address, 10_000_000, currency_code="Coin1", auth_key_prefix=swap_account.auth_key_prefix,
#                  is_blocking=True)
# client.add_currency_to_account(swap_account, "Coin2")
# client.mint_coin(swap_account.address, 10_000_000, currency_code="Coin2", auth_key_prefix=swap_account.auth_key_prefix,
#                  is_blocking=True)
#
# client.swap_add_liquidity(liquidity_account, "LBR", "Coin1", 342423, 435435)
# out = client.swap_get_liquidity_output_amount("Coin1", "LBR", 243244)
# print(out)
