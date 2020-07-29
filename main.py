from libra_client.error import LibraError
from libra_client import Client, Wallet

LibraError.parse_server_code(1)


wallet = Wallet.new()
client = Client("violas_testnet")

module_account = wallet.new_account()
a1 = wallet.new_account()
client.mint_coin(module_account.address, 10_000_000, auth_key_prefix=module_account.auth_key_prefix, is_blocking=True)
try:
    client.transfer_coin(module_account, a1.address, 100)
except LibraError:
    print(1111)
except Exception as e:
    print(type(e))
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
# client.swap_add_liquidity(liquidity_account, "LBR", "Coin1", 3243244, 4354435)
# client.swap_add_liquidity(liquidity_account, "Coin2", "Coin1", 4534452, 2443244)
# out, _ = client.swap_get_swap_input_amount("Coin2", "LBR", 243444)
# bb = client.get_balance(swap_account.address, "LBR")
# client.swap(swap_account, "Coin2", "LBR", out)
# ab = client.get_balance(swap_account.address, "LBR")
# assert ab - bb == 243444