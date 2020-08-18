from violas_client import Client

client = Client("bj_testnet")
print(client.oracle_get_exchange_rate("USD"))