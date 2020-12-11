from violas_client import Client, Wallet
import time

client = Client()
print(client.get_account_state(client.BANK_OWNER_ADDRESS).get_role_id())
