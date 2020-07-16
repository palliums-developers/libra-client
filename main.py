from violas_client import Client
from violas_client.wallet_library import Wallet
from move_core_types.language_storage import core_code_address
from lbrtypes.account_config import association_address

client = Client()
wallet = Wallet.new()
ac = client.get_account_state(association_address())
print(ac)



