from violas_client import Client, Wallet
from violas_client.lbrtypes.transaction.script import Script

client = Client("bj_testnet")

tx = client.get_transaction(4983221)
print(tx.get_sender())

