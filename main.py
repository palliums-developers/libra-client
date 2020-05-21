from uniswap_client import Wallet, Client
from usptypes.bytecode import bytecodes

wallet = Wallet.new()
client = Client()
a1 = wallet.new_account()
a2 = wallet.new_account()

module_account= wallet.new_account()
client.mint_coin(a1.address, 10_000_000, auth_key_prefix=a1.auth_key_prefix, is_blocking=True)
client.mint_coin(a2.address, 10_000_000, auth_key_prefix=a2.auth_key_prefix, is_blocking=True)
client.mint_coin(module_account.address, 10_000_000, auth_key_prefix=module_account.auth_key_prefix, is_blocking=True)

client.publish_token(a1)
client.publish_token(a1, "Violas2")

client.add_currency(1, 2, False, 1_000_000, 100, "Violas1", module_address=a1.address, module_name="Violas1")
client.add_currency(1, 2, False, 1_000_000, 100, "Violas2", module_address=a1.address, module_name="Violas2")

client.add_currency_to_account(a1, a1.address, "Violas1")
client.add_currency_to_account(a2, a1.address, "Violas1")
client.add_currency_to_account(a1, a1.address, "Violas2")
client.add_currency_to_account(a2, a1.address, "Violas2")

client.mint_coin(a1.address, 10_000_000, module_address=a1.address, module_name="Violas1")
# client.mint_coin(a1.address, 10_000_000, module_address=a1.address, module_name="Violas2")
client.mint_coin(a2.address, 10_000_000, module_address=a1.address, module_name="Violas1")
# client.mint_coin(a2.address, 10_000_000, module_address=a1.address, module_name="Violas2")

client.publish_exchange(module_account)
client.set_exchange_module_addres(module_account.address)
client.initialize(module_account)

client.publish_reserve(module_account, a1.address, "Violas1")
# client.publish_reserve(module_account, a1.address, "Violas2")
client.add_liquidity(sender_account=a1, min_liquidity=100, max_token_amount=100_000, violas_amount=100_000, token_module_address=a1.address, token_module_name="Violas1")
print(client.get_balance(a1.address, a1.address, "Violas1"))
client.remove_liquidity(sender_account=a1, amount=90_000, min_violas=10_000, min_tokens=10_000, token_module_address=a1.address, token_module_name="Violas1", exchange_module_address=module_account.address)
print(client.get_balance(a1.address, a1.address, "Violas1"))







