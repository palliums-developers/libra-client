from libra_client import Client, Wallet


client = Client()
wallet = Wallet.new()
a1 = wallet.new_account()
a2 = wallet.new_account()

print(client.get_currency_info("XUS"))