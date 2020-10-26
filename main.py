from violas_client import Client, Wallet
from banktypes.bytecode import CodeType


client = Client()
print(client.get_transaction(16281212))
# wallet = Wallet.new()
# module_account = wallet.new_account()
#
# a1 = wallet.new_account()
# client.mint_coin(a1.address, 2_000_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="USD")
# a2 = wallet.new_account()

# print(client.get_account_state("00000000000000000000000042414e4b").get_designated_dealer_resource())
# seq = client.bank_publish(a1)
# assert client.get_account_transaction(a1.address, seq).get_code_type() == CodeType.PUBLISH
# seq = client.bank_lock(a1, 2_000_000_000, currency_code="USD")
# assert client.get_account_transaction(a1.address, seq).get_code_type() == CodeType.LOCK2
#
# seq = client.bank_borrow(a1, 100_000_000_000-1, currency_code="USD")


