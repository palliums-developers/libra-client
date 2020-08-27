from libra_client import Wallet, Client

wallet = Wallet.new()
a1 = wallet.new_account()
client = Client()
client.mint_coin(a1.address_hex, 11, auth_key_prefix=a1.auth_key_prefix, currency_code="LBR")
client.add_currency_to_account(a1, "Coin1")
client.mint_coin(a1.address_hex, 22, auth_key_prefix=a1.auth_key_prefix, currency_code="Coin1")
balances = client.get_balances(a1.address_hex)
assert balances["LBR"] == 11
assert balances["Coin1"] == 22