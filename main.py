import random
import time
from libra_client import Client, Wallet


client = Client("violas_testnet")
tx = client.get_transaction(1)
print(tx)

