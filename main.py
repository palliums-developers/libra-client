from violas_client import Wallet, Client
from lbrtypes.bytecode import CodeType

client = Client()
wallet = Wallet.new()
a1 = wallet.new_account()
ac = client.get_account_state(a1.address)
txs = client.get_transactions(537000, 1000)
for tx in txs:
    if tx.get_code_type() != CodeType.BLOCK_METADATA:
        print(tx.get_currency_code())