# from violas_client import Client, Wallet
# from violas_client.lbrtypes.account_config import treasury_compliance_account_address, association_address
from exchange_client import Client, Wallet
from lbrtypes.account_config import treasury_compliance_account_address, association_address
import time
from move_core_types.language_storage import core_code_address

client = Client()
wallet = Wallet.new()
a1 = wallet.new_account()
seq = client.mint_coin(a1.address, 10_000_000, auth_key_prefix=a1.auth_key_prefix, is_blocking=True)
seq = client.add_currency_to_account(a1, "Coin1")
print(client.get_account_transaction(a1.address, seq))


