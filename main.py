import random
import time
from violas_client import Client, Wallet
from violas_client.banktypes.bytecode import CodeType


client = Client("bj_testnet")
wallet = Wallet.new()
module_account = wallet.new_account()
client.mint_coin(module_account.address, 200_000_000, auth_key_prefix=module_account.auth_key_prefix,
                 currency_code="vUSDT")
seq = client.bank_publish(module_account)
print(client.get_account_transaction(module_account.address, seq).get_code_type())
