from violas_client import Client, Wallet


client = Client()
wallet = Wallet.new()
a1 = wallet.new_account()
a2 = wallet.new_account()
client.mint_coin(a1.address_hex, 1000, auth_key_prefix=a1.auth_key_prefix, currency_code="LBR")
client.add_currency_to_account(a1, currency_code="Coin1")
client.mint_coin(a1.address_hex, 1000, auth_key_prefix=a1.auth_key_prefix, currency_code="Coin1")
print(client.get_account_state(a1.address_hex))