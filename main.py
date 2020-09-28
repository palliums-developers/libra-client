from libra_client import Client, Wallet

client = Client("libra_testnet")
# wallet = Wallet.new()
# a1 = wallet.new_account()
# client.mint_coin(a1.address, 10000, auth_key_prefix=a1.auth_key_prefix)

balance = client.get_balance("5e5f9844b8486e0c8a719a4cebd36701")
print(balance)
# print(balance)