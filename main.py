from libra_client.client_proxy import Client
from libra.account_config import AccountConfig
from canoser import StrT
address = AccountConfig.association_address()
from libra_client.wallet_library import Wallet

# address = b"1"*16
client = Client()
wallet = Wallet.new()
a1 = wallet.new_account()
a2 = wallet.new_account()
client.mint_coins(a1.address, 100, receiver_auth_key_prefix_opt=a1.auth_key_prefix, is_blocking=True)
client.transfer_coins(a1, 10, a2.address, is_blocking=True, receiver_auth_key_prefix_opt=a2.auth_key_prefix)
print(client.get_balance(a1.address))
print(client.get_balance(a2.address))


