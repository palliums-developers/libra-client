from libra_client import Client, Wallet

client = Client()
wallet = Wallet.new()

a1 = wallet.new_account()
a2 = wallet.new_account()

client.mint_coin(a1.address, 1_000_000, auth_key_prefix=a1.auth_key_prefix)
client.create_child_vasp_account(a1, a2.address, a2.auth_key_prefix, add_all_currency=True)
print(client.get_balances(a2.address))