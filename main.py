import time
from violas_client import Client, Wallet
from violas_client.oracle_client.bytecodes import bytecodes
client = Client("violas_testnet")
tx = client.get_transaction(5009939)
print(tx)
print(tx.get_code_type())
# print(client.get_balances("0135ab4ae628617b11a39ed2058e3930"))
# # print(client.get_account_state("0135ab4ae628617b11a39ed2058e3930"))