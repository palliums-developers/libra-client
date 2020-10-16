from violas_client import Client, Wallet
from lbrtypes.transaction.script import Script

client = Client("bj_testnet")
print(client.get_transaction(4083709).get_receiver())
# wallet = Wallet.new()
# a1 = wallet.new_account()
# a2 = wallet.new_account()
# client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix)
# print(client.get_balances(a1.address_hex))
# client.mint_coin(a2.address, 300_000_000, auth_key_prefix=a2.auth_key_prefix)
# client.bank_publish(a1)
# print(client.bank_is_published(a1.address_hex))

# addr = "ad9d787d68d431d76fc690ec80450213"
# collateral_value = client.bank_get_total_collateral_value(addr)
# borrow_value = client.bank_get_total_borrow_value(addr)
# print(collateral_value, borrow_value)
