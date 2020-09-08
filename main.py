from violas_client import Client
from violas_client.move_core_types.language_storage import core_code_address
from violas_client.lbrtypes.account_config import association_address

bank_module_address = "da13aace1aa1c49e497416a9dd062ecb"
exchange_module_address = "00000000000000000000000045584348"

client = Client("bj_testnet")
client.set_bank_module_address(core_code_address())
client.set_bank_owner_address(bank_module_address)
client.set_exchange_module_address(core_code_address())
client.set_exchange_owner_address(exchange_module_address)

txs = client.get_transactions(23216000, 500)
# client.bank_repay_borrow(a1, currency_code="USD", amount=amount)
# assert client.bank_get_borrow_amount(a1.address, currency_code="USD")[0] == 0