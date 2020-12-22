from bank_client import Client, Wallet

client = Client()
wallet = Wallet.new()
a1 = wallet.new_account()
client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix)
client.bank_publish(a1)
client.add_currency_to_account(a1, "USD")
client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="USD")
client.bank_lock(a1, 100_000_000, currency_code="USD")
print(client.bank_get_lock_amount(a1.address, currency_code="USD"))
# assert approximately_equal_to(client.bank_get_lock_amount(a1.address, currency_code="USD"), 100_000_000)

