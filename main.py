from violas_client import Client, Wallet
from violas_client.banktypes.bytecode import CodeType


client = Client()
wallet = Wallet.new()
module_account = wallet.new_account()

a1 = wallet.new_account()
client.mint_coin(a1.address, 300_000_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="USD")
a2 = wallet.new_account()
client.mint_coin(a2.address, 300_000_000_000, auth_key_prefix=a2.auth_key_prefix, currency_code="USD")
# client.transfer_coin(client.testnet_dd_account, a2.address, 1_000_000_000+1, currency_code='USD')
# client.transfer_coin(a1, a2.address, 1_000_000_000+1, currency_code='USD')



# seq = client.bank_publish(a1)
# assert client.get_account_transaction(a1.address, seq).get_code_type() == CodeType.PUBLISH
#
# seq = client.bank_lock(a1, 200_000_000_000, currency_code="USD")
# assert client.get_account_transaction(a1.address, seq).get_code_type() == CodeType.LOCK2
#
# seq = client.bank_borrow(a1, 100_000_000_000-1, currency_code="USD")


