from violas_client import Client, Wallet


client = Client()
wallet = Wallet.new()
a1 = wallet.new_account()
a2 = wallet.new_account()
client.mint_coin(a1.address, 50, auth_key_prefix=a1.auth_key_prefix)
client.mint_coin(a2.address, 100, auth_key_prefix=a2.auth_key_prefix)

client.transfer_coin(a1, a2.address, 5, is_blocking=True)
client.transfer_coin(a1, a2.address, 10, is_blocking=True)
events = client.get_received_events(a1.address, 0, 10)
print(events)
