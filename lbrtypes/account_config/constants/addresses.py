from lbrtypes.move_core.account_address import AccountAddress
from lbrtypes.on_chain_config import config_address

def association_address() -> AccountAddress :
    return AccountAddress.from_hex("0xA550C18")

def transaction_fee_address() -> AccountAddress :
    return AccountAddress.from_hex("0xFEE")

def validator_set_address() -> AccountAddress:
    return config_address()

def burn_account_address() -> AccountAddress :
    return AccountAddress.from_hex("0xD1E")
