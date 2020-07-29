from violas_client.error import LibraError
from libra_client.error import LibraError as Error

from libra_client import Client as LibraClient
from violas_client import Client, Wallet

LibraError.parse_server_code(1)


wallet = Wallet.new()
client = Client("violas_testnet")

module_account = wallet.new_account()
a1 = wallet.new_account()
client.mint_coin(module_account.address, 10_000_000, auth_key_prefix=module_account.auth_key_prefix, is_blocking=True)

