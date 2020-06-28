# from violas_client import Client, Wallet
# from violas_client.lbrtypes.account_config import treasury_compliance_account_address, association_address
from exchange_client import Client, Wallet
from lbrtypes.account_config import treasury_compliance_account_address, association_address

wallet = Wallet.new()
client = Client()
module_account = wallet.new_account()
client.mint_coin(module_account.address, 10_000_000, auth_key_prefix=module_account.auth_key_prefix,
                 is_blocking=True)
client.swap_publish_contract(module_account)
client.swap_initialize(module_account)
client.set_exchange_module_address(module_account.address)
client.swap_add_currency(module_account, "LBR")
client.swap_add_currency(module_account, "Coin1")
client.swap_add_currency(module_account, "Coin2")

liquidity_account = wallet.new_account()
client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix,
                 is_blocking=True)
client.add_currency_to_account(liquidity_account, "Coin1")
client.mint_coin(liquidity_account.address, 10_000_000, currency_code="Coin1",
                 auth_key_prefix=liquidity_account.auth_key_prefix,
                 is_blocking=True)
client.add_currency_to_account(liquidity_account, "Coin2")
client.mint_coin(liquidity_account.address, 10_000_000, currency_code="Coin2",
                 auth_key_prefix=liquidity_account.auth_key_prefix,
                 is_blocking=True)

swap_account = wallet.new_account()
client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix,
                 is_blocking=True)
client.add_currency_to_account(swap_account, "Coin1")
client.mint_coin(swap_account.address, 10_000_000, currency_code="Coin1",
                 auth_key_prefix=swap_account.auth_key_prefix,
                 is_blocking=True)
client.add_currency_to_account(swap_account, "Coin2")
client.mint_coin(swap_account.address, 10_000_000, currency_code="Coin2",
                 auth_key_prefix=swap_account.auth_key_prefix,
                 is_blocking=True)

client.swap_add_liquidity(liquidity_account, "LBR", "Coin1", 200_000, 100_000)
expected_amount = client.swap_get_expected_liquidity_amount("Coin1", "LBR", 100)
client.swap_add_liquidity(liquidity_account, "Coin1", "LBR", 100, 100_000)
assert client.get_balance(liquidity_account.address, "LBR") == 10_000_000 - 200_000 - expected_amount


