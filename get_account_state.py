import argparse
from violas_client import Client

parser = argparse.ArgumentParser()
parser.add_argument("address")
args = parser.parse_args()
client = Client("bj_testnet")
print(client.get_account_state(args.address))
