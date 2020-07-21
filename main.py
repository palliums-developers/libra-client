from violas_client import Client
from violas_client.wallet_library import Wallet
from move_core_types.language_storage import core_code_address
from lbrtypes.account_config import association_address, transaction_fee_address
from banktypes.bytecode import bytecodes, CodeType

wallet = Wallet.new()
module_account = wallet.new_account()
client = Client()
client.mint_coin(module_account.address, 2_000_000_000, auth_key_prefix=module_account.auth_key_prefix)
seq = client.bank_publish_contract(module_account)
assert client.get_account_transaction(module_account.address, seq).get_amount() == None
client.set_bank_module_address(module_account.address)
seq = client.bank_publish(module_account)
assert client.get_account_transaction(module_account.address, seq).get_amount() == None

seq = client.bank_register_token(module_account, module_account.address, 0.5, currency_code="LBR")
assert client.get_account_transaction(module_account.address, seq).get_amount() == None
seq = client.bank_update_price(module_account, 0.1, currency_code="LBR")
assert client.get_account_transaction(module_account.address, seq).get_amount() == None

a1 = wallet.new_account()
client.mint_coin(a1.address, 3_000_000_000, auth_key_prefix=a1.auth_key_prefix)
seq = client.bank_publish(a1)
assert client.get_account_transaction(a1.address, seq).get_amount() == None
seq = client.bank_enter(a1, 2_000_000_000, currency_code="LBR")
assert client.get_account_transaction(a1.address, seq).get_amount() == 2_000_000_000

seq = client.bank_lock(a1, 1_000_000_000, currency_code="LBR")
assert client.get_account_transaction(a1.address, seq).get_amount() == 1_000_000_000

seq = client.bank_borrow(a1, 10_000_000, currency_code="LBR")
assert client.get_account_transaction(a1.address, seq).get_amount() == 10_000_000

seq = client.bank_repay_borrow(a1, amount=100, currency_code="LBR")
assert client.get_account_transaction(a1.address, seq).get_amount() == 100

seq = client.bank_redeem(a1, currency_code="LBR", amount=100)
assert client.get_account_transaction(a1.address, seq).get_amount() == 100

seq = client.bank_exit(a1, 1_000_000_000, currency_code="LBR")
assert client.get_account_transaction(a1.address, seq).get_amount() == 1_000_000_000