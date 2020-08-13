from libra_client import Client, Wallet
from lbrtypes.account_config.constants.addresses import testnet_dd_account_address

# wallet = Wallet.new()
# a1 = wallet.new_account()
client = Client("libra_testnet")
print(client.get_latest_version())
