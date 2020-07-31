from violas_client import Client, Wallet
from violas_client.lbrtypes.account_config.constants.addresses import transaction_fee_address, testnet_dd_account_address
# # from libra_client.wallet_library import Wallet
import json

client = Client("bj_testnet")
wallet = Wallet.new()
a1 = wallet.new_account()
a2 = wallet.new_account()
seq = client.mint_coin(a1.address, 1_000_000, auth_key_prefix=a1.auth_key_prefix, is_blocking=True)
j = client.get_account_transaction(testnet_dd_account_address(), seq).to_json()
print(j)


