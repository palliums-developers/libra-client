from violas_client import Client, Wallet

client = Client()
wallet = Wallet.new()
a1 = wallet.new_account()
client.mint_coin(a1.address, 100, auth_key_prefix=a1.auth_key_prefix)
print(client.get_balances(a1.address))