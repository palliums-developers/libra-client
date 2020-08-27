from libra_client import Wallet, Client

client = Client()
wallet = Wallet.new()
a1 = wallet.new_account()
ac = client.get_account_state(a1.address)
assert None == ac
client.mint_coin(a1.address, 100, auth_key_prefix=a1.auth_key_prefix)
print(client.get_balances(a1.address))
# ac = client.get_account_state(a1.address)
# assert None != ac