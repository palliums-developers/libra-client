from libra_client import Client, Wallet


client = Client("violas_testnet")
wallet = Wallet.new()
a1 = wallet.new_account()
client.mint_coin(a1.address_hex, 100, auth_key_prefix=a1.auth_key_prefix)


