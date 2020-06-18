from libra_client import Client, Wallet

client = Client()
wallet = Wallet.new()
a1 = wallet.new_account()
client.mint_coin(a1.address, 10000000, auth_key_prefix=a1.auth_key_prefix, currency_code="VLSUSD")
client.add_currency_to_account(a1, "LBREUR", gas_currency_code="VLSUSD")
client.mint_coin(a1.address, 10000000, auth_key_prefix=a1.auth_key_prefix, currency_code="LBREUR")

