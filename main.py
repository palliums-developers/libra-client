from uniswap_client import Wallet, Client
from usptypes.bytecode import bytecodes
from lbrtypes.account_config import association_address

wallet = Wallet.new()
client = Client()
module_account = wallet.new_account()
client.mint_coin(module_account.address, 10_000_000, auth_key_prefix=module_account.auth_key_prefix,
                 is_blocking=True)
client.publish_exchange(module_account)
client.set_exchange_module_addres(module_account.address)
client.initialize(module_account)
client.publish_reserve(module_account, "Coin1")

liquidity_account = wallet.new_account()
client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix,
                 is_blocking=True)
client.add_currency_to_account(liquidity_account, "Coin1")
client.mint_coin(liquidity_account.address, 10_000_000, module_name="Coin1",
                 auth_key_prefix=liquidity_account.auth_key_prefix,
                 is_blocking=True)
client.add_liquidity(liquidity_account, 1, 1_000_000, 1_000_000, "Coin1")
swap_account = liquidity_account
violas_balance = client.get_balance(swap_account.address)
token_blance = client.get_balance(swap_account.address, "Coin1")

print(violas_balance, token_blance)

client.violas_to_token_swap(swap_account, 100_000, 1, "Coin1", exchange_module_address=module_account.address)

violas_balance = client.get_balance(swap_account.address)
token_blance = client.get_balance(swap_account.address, "Coin1")

print(violas_balance, token_blance)

# assert client.get_balance(swap_account.address) == violas_balance - 10_000
# assert client.get_balance(swap_account.address, "Coin1") == token_blance + 10_000 - 1










