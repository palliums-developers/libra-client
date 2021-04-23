import random
import time
from violas_client import Client, Wallet


import argparse
from violas_client import Client


client = Client("violas_testnet")
print(client.get_parent_vasp("bca6a80719ad60106aa35683a98d389e"))