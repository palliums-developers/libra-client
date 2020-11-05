from violas_client import Client, Wallet
from violas_client.banktypes.bytecode import CodeType
import time

client = Client()
wallet = Wallet.new()
a1 = wallet.new_account()
client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="USD")
client.bank_publish(a1)
client.bank_lock(a1, 100_000_000, currency_code="USD")
client.bank_borrow(a1, 10_000_000, currency_code="USD")
borrow_rate = client.bank_get_borrow_rate(currency_code="USD")
time.sleep(120)
_, borrow_amount = client.bank_get_borrow_amount(a1.address, currency_code="USD")
print(borrow_amount, 10_000_000 + 10_000_000 * borrow_rate * 2)
client.bank_repay_borrow(a1, amount=borrow_amount, currency_code="USD")
assert client.bank_get_borrow_amount(a1.address, "USD")[0] == 0
