from libra_client import Client, Wallet

client = Client("bj_testnet")
# wallet = Wallet.new()
# a1 = wallet.new_account()
# client.mint_coin(a1.address, 10000, auth_key_prefix=a1.auth_key_prefix)

balance = client.get_balance("fec9e6e216105d40132e368c7046ed1c")
print(balance)
# print(balance)