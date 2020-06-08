import argparse
from compound_client import Client

module_address=""

parser = argparse.ArgumentParser()
parser.add_argument("address")
args = parser.parse_args()
client = Client.new(url="http://47.93.114.230:50001")
client.set_bank_module_address(module_address)
client.get_account_state(args.address)
