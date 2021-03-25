import random
import time
from violas_client import Client, Wallet


client = Client("violas_testnet")
addr = b'\xb1K\xc3(nK\x9bA\xc8`"\xf2\xe6\x14\xd7!'
print(client.bank_is_published(addr))