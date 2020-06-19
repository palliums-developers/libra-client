from libra_client import Client, Wallet
from libra_client.lbrtypes.account_config import association_address


client = Client()
print(client.get_account_transaction(association_address(), 1))
# wallet = Wallet.new()
# a1 = wallet.new_account()
# seq = client.mint_coin(a1.address, 10000000, auth_key_prefix=a1.auth_key_prefix, currency_code="VLSUSD")
# print(client.get_g)
# client.add_currency_to_account(a1, "LBREUR", gas_currency_code="VLSUSD")
# client.mint_coin(a1.address, 10000000, auth_key_prefix=a1.auth_key_prefix, currency_code="LBREUR")

