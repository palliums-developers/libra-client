from libra_client import Client, Wallet
from lbrtypes.account_config import association_address
from test import create_accounts, create_client, create_accounts_with_coins

client = create_client()
[a1, a2] = create_accounts(2)
seq = client.mint_coin(a1.address, 100, auth_key_prefix=a1.auth_key_prefix, is_blocking=True, coin_currency="Coin1")
seq = client.mint_coin(a2.address, 100, auth_key_prefix=a2.auth_key_prefix, is_blocking=True, coin_currency="Coin1")

print(client.get_account_state(a2.address))

seq = client.transfer_coin(a1, a2.address, 10, auth_key_prefix=a2.auth_key_prefix, is_blocking=True, coin_currency="Coin1")












