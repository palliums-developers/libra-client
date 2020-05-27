from compound_client import Client, Wallet
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("address")
args = parser.parse_args()
address = args.address

client = Client()
print(client.get_account_state(address))














