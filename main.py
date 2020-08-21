from libra_client import Client, Wallet
dd = "000000000000000000000000000000dd"
client = Client()
print(client.get_latest_version())
# wallet = Wallet.new()
# a1 = wallet.new_account()
# ac = client.get_account_state(a1.address)
# assert None == ac
# client.mint_coin(a1.address, 100, auth_key_prefix=a1.auth_key_prefix)
# ac = client.get_account_state(a1.address)
# assert None != ac