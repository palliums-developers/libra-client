from test import create_accounts, create_client

[a1] = create_accounts(1)
client = create_client()
balance = client.get_balance(a1.address)
assert balance == 0

client.mint_coin(a1.address, 100, receiver_auth_key_prefix_opt=a1.auth_key_prefix, is_blocking=True)
balance = client.get_balance(a1.address)
assert balance == 100


