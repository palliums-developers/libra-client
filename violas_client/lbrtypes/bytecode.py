from enum import IntEnum
from lbrtypes.move_core.account_address import AccountAddress

class TransactionType(IntEnum):
    SIGNED_TRANSACTION = 0
    CHANGE_SET = 1
    BLOCK_METADATA = 2

class CodeType(IntEnum):
    ADD_CURRENCY_TO_ACCOUNT = 0
    ADD_VALIDATOR = 1
    BURN = 2
    BURN_TXN_FEES = 3
    CANCEL_BURN = 4
    CREATE_CHILD_VASP_ACCOUNT = 5
    CREATE_DESIGNATED_DEALER = 6
    CREATE_PARENT_VASP_ACCOUNT = 7
    CREATE_VALIDATOR_ACCOUNT = 8
    EMPTY_SCRIPT = 9
    FREEZE_ACCOUNT = 10
    MINT_LBR = 11
    MINT_LBR_TO_ADDRESS = 12
    MINT = 13
    MODIFY_PUBLISHING_OPTION = 14
    PEER_TO_PEER_WITH_METADATA = 15
    PREBURN = 16
    PUBLISH_SHARED_ED25519_PUBLIC_KEY = 17
    REGISTER_PREBURNER = 18
    REGISTER_VALIDATOR = 19
    REMOVE_ASSOCIATION_PRIVILEGE = 20
    REMOVE_VALIDATOR = 21
    ROTATE_AUTHENTICATION_KEY = 22
    ROTATE_AUTHENTICATION_KEY_WITH_NONCE = 23
    ROTATE_BASE_URL = 24
    ROTATE_COMPLIANCE_PUBLIC_KEY = 25
    ROTATE_CONSENSUS_PUBKEY = 26
    ROTATE_SHARED_ED25519_PUBLIC_KEY = 27
    ROTATE_VALIDATOR_CONFIG = 28
    TIERED_MINT = 29
    UNFREEZE_ACCOUNT = 30
    UNMINT_LBR = 31
    UPDATE_EXCHANGE_RATE = 32
    UPDATE_LIBRA_VERSION = 33
    UPDATE_MINTING_ABILITY = 34

    CHANGE_SET = 97
    BLOCK_METADATA = 98

    UNKNOWN = 100

bytecodes = {
    "add_currency_to_account": b'\xa1\x1c\xeb\x0b\x01\x00\x07\x01F\x00\x00\x00\x02\x00\x00\x00\x03H\x00\x00\x00\x06\x00\x00\x00\x04N\x00\x00\x00\x02\x00\x00\x00\x05P\x00\x00\x00\x07\x00\x00\x00\x07W\x00\x00\x00\x1a\x00\x00\x00\x08q\x00\x00\x00\x10\x00\x00\x00\t\x81\x00\x00\x00\x0b\x00\x00\x00\x00\x00\x00\x01\x00\x01\x01\x01\x00\x02\x01\x06\x0c\x00\x01\t\x00\x0cLibraAccount\x0cadd_currency\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x00\x01\x03\x00\x0b\x008\x00\x02',
    "add_validator": b'\xa1\x1c\xeb\x0b\x01\x00\x06\x01=\x00\x00\x00\x02\x00\x00\x00\x03?\x00\x00\x00\x05\x00\x00\x00\x05D\x00\x00\x00\x05\x00\x00\x00\x07I\x00\x00\x00\x1a\x00\x00\x00\x08c\x00\x00\x00\x10\x00\x00\x00\ts\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00\x02\x06\x0c\x05\x00\x0bLibraSystem\radd_validator\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x04\x00\x0b\x00\n\x01\x11\x00\x02',
    "burn": b'\xa1\x1c\xeb\x0b\x01\x00\x07\x01F\x00\x00\x00\x04\x00\x00\x00\x03J\x00\x00\x00\x0b\x00\x00\x00\x04U\x00\x00\x00\x02\x00\x00\x00\x05W\x00\x00\x00\x11\x00\x00\x00\x07h\x00\x00\x00.\x00\x00\x00\x08\x96\x00\x00\x00\x10\x00\x00\x00\t\xa6\x00\x00\x00\x13\x00\x00\x00\x00\x00\x00\x01\x01\x02\x00\x01\x00\x00\x03\x02\x01\x01\x01\x01\x04\x02\x06\x0c\x03\x00\x02\x06\x0c\x05\x03\x06\x0c\x03\x05\x01\t\x00\x05Libra\x0cSlidingNonce\x15record_nonce_or_abort\x04burn\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x03\x01\x07\x00\n\x00\n\x01\x11\x00\x0b\x00\n\x028\x00\x02',
    "burn_txn_fees": b'\xa1\x1c\xeb\x0b\x01\x00\x08\x01O\x00\x00\x00\x08\x00\x00\x00\x02W\x00\x00\x00\r\x00\x00\x00\x03d\x00\x00\x00\x1e\x00\x00\x00\x04\x82\x00\x00\x00\x16\x00\x00\x00\x05\x98\x00\x00\x006\x00\x00\x00\x07\xce\x00\x00\x00\x7f\x00\x00\x00\x08M\x01\x00\x00\x10\x00\x00\x00\t]\x01\x00\x00L\x00\x00\x00\x00\x00\x00\x01\x00\x02\x00\x03\x02\x04\x01\x01\x01\x00\x07\x02\x00\x01\x07\x02\x00\x02\x05\x00\x01\x01\x01\x02\x06\x02\x03\x01\x01\x03\x08\x04\x01\x01\x01\x03\t\x01\x05\x01\x01\x03\n\x02\x01\x01\x01\x04\x07\x03\x07\x01\x08\x01\t\x02\x08\x02\t\x00\x08\x00\t\x01\x07\x02\x07\x00\x07\x02\x06\x0c\x0b\x00\x01\t\x00\x00\x01\x06\x0c\x01\x0b\x00\x01\t\x00\x02\x06\x0c\x06\x0b\x00\x01\t\x00\x01\x01\x03\x0b\x00\x01\t\x00\x0b\x00\x01\x08\x01\x0b\x00\x01\x08\x02\x01\t\x00\x01\x08\x01\x01\x08\x02\x05Coin1\x05Coin2\x05Libra\x0eTransactionFee\x0eBurnCapability\x17publish_burn_capability\x16remove_burn_capability\x01T\tburn_fees\x06is_lbr\x0cpreburn_fees\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x02\x06"\x00\n\x008\x008\x01\x03\x05\x00\x05\x18\x00\n\x008\x02\x0c\x02\n\x008\x03\x0c\x03\n\x00\x0e\x028\x04\n\x00\x0e\x038\x05\n\x00\x0b\x028\x06\x0b\x00\x0b\x038\x07\x05!\x00\n\x008\x08\x0c\x01\n\x00\x0e\x018\t\x0b\x00\x0b\x018\n\x02',
    "cancel_burn": b'\xa1\x1c\xeb\x0b\x01\x00\x07\x01F\x00\x00\x00\x02\x00\x00\x00\x03H\x00\x00\x00\x06\x00\x00\x00\x04N\x00\x00\x00\x02\x00\x00\x00\x05P\x00\x00\x00\x08\x00\x00\x00\x07X\x00\x00\x00\x19\x00\x00\x00\x08q\x00\x00\x00\x10\x00\x00\x00\t\x81\x00\x00\x00\r\x00\x00\x00\x00\x00\x00\x01\x00\x01\x01\x01\x00\x02\x02\x06\x0c\x05\x00\x01\t\x00\x0cLibraAccount\x0bcancel_burn\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x00\x01\x04\x00\x0b\x00\n\x018\x00\x02',
    "create_child_vasp_account": b'\xa1\x1c\xeb\x0b\x01\x00\x07\x01F\x00\x00\x00\x02\x00\x00\x00\x03H\x00\x00\x00\x0c\x00\x00\x00\x04T\x00\x00\x00\x04\x00\x00\x00\x05X\x00\x00\x00\x18\x00\x00\x00\x07p\x00\x00\x000\x00\x00\x00\x08\xa0\x00\x00\x00\x10\x00\x00\x00\t\xb0\x00\x00\x001\x00\x00\x00\x00\x00\x00\x01\x00\x01\x01\x01\x00\x02\x02\x01\x01\x01\x00\x04\x01\x04\x04\x06\x0c\x05\n\x02\x01\x00\x03\x06\x0c\x05\x03\x05\x06\x0c\x05\n\x02\x01\x03\x01\t\x00\x0cLibraAccount\x19create_child_vasp_account\x08pay_from\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x03\x01\x12\x00\n\x00\n\x01\x0b\x02\n\x038\x00\n\x04\x06\x00\x00\x00\x00\x00\x00\x00\x00$\x03\n\x00\x05\x0f\x00\x0b\x00\n\x01\n\x048\x01\x05\x11\x00\x0b\x00\x01\x02',
    "create_designated_dealer": b'\xa1\x1c\xeb\x0b\x01\x00\x07\x01F\x00\x00\x00\x04\x00\x00\x00\x03J\x00\x00\x00\x0b\x00\x00\x00\x04U\x00\x00\x00\x02\x00\x00\x00\x05W\x00\x00\x00\x15\x00\x00\x00\x07l\x00\x00\x00I\x00\x00\x00\x08\xb5\x00\x00\x00\x10\x00\x00\x00\t\xc5\x00\x00\x00\x15\x00\x00\x00\x00\x00\x00\x01\x01\x02\x00\x01\x00\x00\x03\x02\x01\x01\x01\x01\x04\x02\x06\x0c\x03\x00\x03\x06\x0c\x05\n\x02\x04\x06\x0c\x03\x05\n\x02\x01\t\x00\x0cLibraAccount\x0cSlidingNonce\x15record_nonce_or_abort\x18create_designated_dealer\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x03\x01\x08\x00\n\x00\n\x01\x11\x00\x0b\x00\n\x02\x0b\x038\x00\x02',
    "create_parent_vasp_account": b'\xa1\x1c\xeb\x0b\x01\x00\x07\x01F\x00\x00\x00\x02\x00\x00\x00\x03H\x00\x00\x00\x06\x00\x00\x00\x04N\x00\x00\x00\x02\x00\x00\x00\x05P\x00\x00\x00\x11\x00\x00\x00\x07a\x00\x00\x00(\x00\x00\x00\x08\x89\x00\x00\x00\x10\x00\x00\x00\t\x99\x00\x00\x00\x17\x00\x00\x00\x00\x00\x00\x01\x00\x01\x01\x01\x00\x02\x07\x06\x0c\x05\n\x02\n\x02\n\x02\n\x02\x01\x00\x01\t\x00\x0cLibraAccount\x1acreate_parent_vasp_account\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x00\x01\t\x00\x0b\x00\n\x01\x0b\x02\x0b\x03\x0b\x04\x0b\x05\n\x068\x00\x02',
    "create_validator_account": b'\xa1\x1c\xeb\x0b\x01\x00\x07\x01F\x00\x00\x00\x02\x00\x00\x00\x03H\x00\x00\x00\x06\x00\x00\x00\x04N\x00\x00\x00\x02\x00\x00\x00\x05P\x00\x00\x00\n\x00\x00\x00\x07Z\x00\x00\x00&\x00\x00\x00\x08\x80\x00\x00\x00\x10\x00\x00\x00\t\x90\x00\x00\x00\x0f\x00\x00\x00\x00\x00\x00\x01\x00\x01\x01\x01\x00\x02\x03\x06\x0c\x05\n\x02\x00\x01\t\x00\x0cLibraAccount\x18create_validator_account\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x00\x01\x05\x00\x0b\x00\n\x01\x0b\x028\x00\x02',
    "empty_script": b'\xa1\x1c\xeb\x0b\x01\x00\x02\x05\x19\x00\x00\x00\x01\x00\x00\x00\t\x1a\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x01\x00\x02',
    "freeze_account": b'\xa1\x1c\xeb\x0b\x01\x00\x06\x01=\x00\x00\x00\x04\x00\x00\x00\x03A\x00\x00\x00\n\x00\x00\x00\x05K\x00\x00\x00\x0e\x00\x00\x00\x07Y\x00\x00\x00?\x00\x00\x00\x08\x98\x00\x00\x00\x10\x00\x00\x00\t\xa8\x00\x00\x00\x12\x00\x00\x00\x00\x00\x00\x01\x01\x02\x00\x01\x00\x00\x03\x02\x01\x00\x02\x06\x0c\x03\x00\x02\x06\x0c\x05\x03\x06\x0c\x03\x05\x0cLibraAccount\x0cSlidingNonce\x15record_nonce_or_abort\x0efreeze_account\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x01\x07\x00\n\x00\n\x01\x11\x00\x0b\x00\n\x02\x11\x01\x02',
    "mint_lbr": b'\xa1\x1c\xeb\x0b\x01\x00\x08\x01O\x00\x00\x00\x0c\x00\x00\x00\x02[\x00\x00\x00\x11\x00\x00\x00\x03l\x00\x00\x00\x1c\x00\x00\x00\x04\x88\x00\x00\x00\x0e\x00\x00\x00\x05\x96\x00\x00\x00\\\x00\x00\x00\x07\xf2\x00\x00\x00_\x00\x00\x00\x08Q\x01\x00\x00\x10\x00\x00\x00\ta\x01\x00\x00H\x00\x00\x00\x00\x00\x00\x01\x00\x02\x00\x03\x00\x04\x00\x05\x03\x07\x01\x01\x01\x00\x07\x02\x00\x01\x07\x02\x00\x02\x07\x01\x00\x05\x06\x00\x01\x00\x02\x08\x02\x03\x00\x04\t\x01\x04\x01\x01\x04\n\x05\x06\x01\x01\x04\x0b\x07\x08\x01\x01\x02\n\x02\x0b\x04\n\x04\x0b\x03\x0c\x03\n\x03\x0b\x01\x06\x0c\x01\x05\x03\x03\x0b\x00\x01\x08\x01\x0b\x00\x01\x08\x02\x03\x0b\x00\x01\x08\x03\x0b\x00\x01\x08\x01\x0b\x00\x01\x08\x02\x01\x03\x02\x06\x0c\x0b\x00\x01\t\x00\x00\x02\x06\x0c\x03\x01\x0b\x00\x01\t\x00\x08\x0b\x00\x01\x08\x01\x0b\x00\x01\x08\x01\x03\x0b\x00\x01\x08\x02\x0b\x00\x01\x08\x02\x03\x0b\x00\x01\x08\x03\x05\x01\x08\x01\x01\x08\x02\x01\x08\x03\x05Coin1\x05Coin2\x03LBR\x05Libra\x0cLibraAccount\x06Signer\naddress_of\x01T\x06create\x07balance\ndeposit_to\rwithdraw_from\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\t"\x00\n\x00\x11\x00\x0c\t\n\t8\x00\x0c\x04\n\t8\x01\x0c\x07\n\x00\n\x048\x02\x0c\x02\n\x00\n\x078\x03\x0c\x05\n\x01\x0b\x02\x0b\x05\x11\x01\x0c\x06\x0c\x03\x0c\x08\n\x00\x0b\x088\x04\n\x00\x0b\x038\x05\x0b\x00\x0b\x068\x06\x02',
    "mint_lbr_to_address": b'\xa1\x1c\xeb\x0b\x01\x00\x08\x01O\x00\x00\x00\x04\x00\x00\x00\x02S\x00\x00\x00\x04\x00\x00\x00\x03W\x00\x00\x00\x10\x00\x00\x00\x04g\x00\x00\x00\x02\x00\x00\x00\x05i\x00\x00\x00\x18\x00\x00\x00\x07\x81\x00\x00\x00E\x00\x00\x00\x08\xc6\x00\x00\x00\x10\x00\x00\x00\t\xd6\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x01\x00\x02\x01\x00\x01\x03\x00\x01\x01\x01\x01\x04\x02\x03\x00\x01\x05\x04\x01\x00\x00\x06\x02\x05\n\x02\x00\x01\x05\x01\x01\x03\x06\x0c\x05\x03\x04\x06\x0c\x05\n\x02\x03\x01\x08\x00\x03LBR\x0cLibraAccount\x01T\x16create_testnet_account\x06exists\x13mint_lbr_to_address\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x01\r\x00\n\x01\x11\x01 \x03\x05\x00\x05\x08\x00\n\x01\x0b\x028\x00\x0b\x00\n\x01\n\x03\x11\x02\x02',
    "mint": b'\xa1\x1c\xeb\x0b\x01\x00\x07\x01F\x00\x00\x00\x02\x00\x00\x00\x03H\x00\x00\x00\x11\x00\x00\x00\x04Y\x00\x00\x00\x04\x00\x00\x00\x05]\x00\x00\x00\x18\x00\x00\x00\x07u\x00\x00\x00;\x00\x00\x00\x08\xb0\x00\x00\x00\x10\x00\x00\x00\t\xc0\x00\x00\x00 \x00\x00\x00\x00\x00\x00\x01\x00\x01\x01\x01\x00\x02\x02\x03\x00\x00\x03\x04\x01\x01\x01\x00\x06\x02\x06\x02\x05\n\x02\x00\x01\x05\x01\x01\x03\x06\x0c\x05\x03\x04\x06\x0c\x05\n\x02\x03\x01\t\x00\x0cLibraAccount\x16create_testnet_account\x06exists\x0fmint_to_address\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x05\x01\r\x00\n\x01\x11\x01 \x03\x05\x00\x05\x08\x00\n\x01\x0b\x028\x00\x0b\x00\n\x01\n\x038\x01\x02',
    "modify_publishing_option": b'\xa1\x1c\xeb\x0b\x01\x00\x06\x01=\x00\x00\x00\x02\x00\x00\x00\x03?\x00\x00\x00\x05\x00\x00\x00\x05D\x00\x00\x00\x06\x00\x00\x00\x07J\x00\x00\x00$\x00\x00\x00\x08n\x00\x00\x00\x10\x00\x00\x00\t~\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00\x02\x06\x0c\n\x02\x00\rLibraVMConfig\x15set_publishing_option\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x04\x00\x0b\x00\x0b\x01\x11\x00\x02',
    "peer_to_peer_with_metadata": b'\xa1\x1c\xeb\x0b\x01\x00\x07\x01F\x00\x00\x00\x02\x00\x00\x00\x03H\x00\x00\x00\x06\x00\x00\x00\x04N\x00\x00\x00\x02\x00\x00\x00\x05P\x00\x00\x00\r\x00\x00\x00\x07]\x00\x00\x00$\x00\x00\x00\x08\x81\x00\x00\x00\x10\x00\x00\x00\t\x91\x00\x00\x00\x13\x00\x00\x00\x00\x00\x00\x01\x00\x01\x01\x01\x00\x02\x05\x06\x0c\x05\x03\n\x02\n\x02\x00\x01\t\x00\x0cLibraAccount\x16pay_from_with_metadata\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x00\x01\x07\x00\x0b\x00\n\x01\n\x02\x0b\x03\x0b\x048\x00\x02',
    "preburn": b'\xa1\x1c\xeb\x0b\x01\x00\x08\x01O\x00\x00\x00\x04\x00\x00\x00\x02S\x00\x00\x00\x05\x00\x00\x00\x03X\x00\x00\x00\x0c\x00\x00\x00\x04d\x00\x00\x00\x04\x00\x00\x00\x05h\x00\x00\x00\x16\x00\x00\x00\x07~\x00\x00\x00.\x00\x00\x00\x08\xac\x00\x00\x00\x10\x00\x00\x00\t\xbc\x00\x00\x00\x11\x00\x00\x00\x00\x00\x00\x01\x00\x02\x01\x01\x01\x00\x03\x00\x01\x01\x01\x01\x04\x02\x03\x01\x01\x01\x04\x00\x04\x02\x06\x0c\x0b\x00\x01\t\x00\x00\x02\x06\x0c\x03\x01\x0b\x00\x01\t\x00\x01\t\x00\x05Libra\x0cLibraAccount\x01T\npreburn_to\rwithdraw_from\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x02\x01\x06\x00\n\x00\x0b\x00\n\x018\x008\x01\x02',
    "publish_shared_ed25519_public_key": b'\xa1\x1c\xeb\x0b\x01\x00\x06\x01=\x00\x00\x00\x02\x00\x00\x00\x03?\x00\x00\x00\x05\x00\x00\x00\x05D\x00\x00\x00\x06\x00\x00\x00\x07J\x00\x00\x00\x1f\x00\x00\x00\x08i\x00\x00\x00\x10\x00\x00\x00\ty\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00\x02\x06\x0c\n\x02\x00\x16SharedEd25519PublicKey\x07publish\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x04\x00\x0b\x00\x0b\x01\x11\x00\x02',
    "register_preburner": b'\xa1\x1c\xeb\x0b\x01\x00\x08\x01O\x00\x00\x00\x02\x00\x00\x00\x02Q\x00\x00\x00\x05\x00\x00\x00\x03V\x00\x00\x00\x0c\x00\x00\x00\x04b\x00\x00\x00\x04\x00\x00\x00\x05f\x00\x00\x00\x15\x00\x00\x00\x07{\x00\x00\x00*\x00\x00\x00\x08\xa5\x00\x00\x00\x10\x00\x00\x00\t\xb5\x00\x00\x00\r\x00\x00\x00\x00\x00\x00\x01\x01\x01\x01\x00\x02\x00\x01\x01\x01\x00\x03\x02\x00\x01\x01\x00\x04\x01\x04\x00\x01\x0b\x00\x01\t\x00\x02\x06\x0c\x0b\x00\x01\t\x00\x01\x06\x0c\x01\t\x00\x05Libra\x07Preburn\x0bnew_preburn\x0fpublish_preburn\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x03\x00\x04\x00\x0b\x008\x008\x01\x02',
    "register_validator": b'\xa1\x1c\xeb\x0b\x01\x00\x06\x01=\x00\x00\x00\x06\x00\x00\x00\x03C\x00\x00\x00\x0f\x00\x00\x00\x05R\x00\x00\x00%\x00\x00\x00\x07w\x00\x00\x00G\x00\x00\x00\x08\xbe\x00\x00\x00\x10\x00\x00\x00\t\xce\x00\x00\x00"\x00\x00\x00\x00\x00\x00\x01\x00\x02\x01\x03\x00\x01\x00\x02\x04\x02\x03\x00\x00\x05\x04\x03\x00\x01\x06\x0c\x01\x05\x07\x06\x0c\x05\n\x02\n\x02\n\x02\n\x02\n\x02\x00\x02\x06\x0c\x05\x06\x06\x0c\n\x02\n\x02\n\x02\n\x02\n\x02\x0bLibraSystem\x06Signer\x0fValidatorConfig\naddress_of\nset_config\radd_validator\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x01\x0f\x00\n\x00\x11\x00\x0c\x06\n\x00\n\x06\x0b\x01\x0b\x02\x0b\x03\x0b\x04\x0b\x05\x11\x01\x0b\x00\n\x06\x11\x02\x02',
    "remove_association_privilege": b'\xa1\x1c\xeb\x0b\x01\x00\x07\x01F\x00\x00\x00\x02\x00\x00\x00\x03H\x00\x00\x00\x06\x00\x00\x00\x04N\x00\x00\x00\x02\x00\x00\x00\x05P\x00\x00\x00\x08\x00\x00\x00\x07X\x00\x00\x00\x1d\x00\x00\x00\x08u\x00\x00\x00\x10\x00\x00\x00\t\x85\x00\x00\x00\r\x00\x00\x00\x00\x00\x00\x01\x00\x01\x01\x01\x00\x02\x02\x06\x0c\x05\x00\x01\t\x00\x0bAssociation\x10remove_privilege\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x00\x01\x04\x00\x0b\x00\n\x018\x00\x02',
    "remove_validator": b'\xa1\x1c\xeb\x0b\x01\x00\x06\x01=\x00\x00\x00\x02\x00\x00\x00\x03?\x00\x00\x00\x05\x00\x00\x00\x05D\x00\x00\x00\x05\x00\x00\x00\x07I\x00\x00\x00\x1d\x00\x00\x00\x08f\x00\x00\x00\x10\x00\x00\x00\tv\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00\x02\x06\x0c\x05\x00\x0bLibraSystem\x10remove_validator\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x04\x00\x0b\x00\n\x01\x11\x00\x02',
    "rotate_authentication_key": b"\xa1\x1c\xeb\x0b\x01\x00\x06\x01=\x00\x00\x00\x02\x00\x00\x00\x03?\x00\x00\x00\x05\x00\x00\x00\x05D\x00\x00\x00\x06\x00\x00\x00\x07J\x00\x00\x00'\x00\x00\x00\x08q\x00\x00\x00\x10\x00\x00\x00\t\x81\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00\x02\x06\x0c\n\x02\x00\x0cLibraAccount\x19rotate_authentication_key\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x04\x00\x0b\x00\x0b\x01\x11\x00\x02",
    "rotate_authentication_key_with_nonce": b'\xa1\x1c\xeb\x0b\x01\x00\x06\x01=\x00\x00\x00\x04\x00\x00\x00\x03A\x00\x00\x00\n\x00\x00\x00\x05K\x00\x00\x00\x10\x00\x00\x00\x07[\x00\x00\x00J\x00\x00\x00\x08\xa5\x00\x00\x00\x10\x00\x00\x00\t\xb5\x00\x00\x00\x12\x00\x00\x00\x00\x00\x00\x01\x01\x02\x00\x01\x00\x00\x03\x02\x01\x00\x02\x06\x0c\x03\x00\x02\x06\x0c\n\x02\x03\x06\x0c\x03\n\x02\x0cLibraAccount\x0cSlidingNonce\x15record_nonce_or_abort\x19rotate_authentication_key\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x01\x07\x00\n\x00\n\x01\x11\x00\x0b\x00\x0b\x02\x11\x01\x02',
    "rotate_base_url": b'\xa1\x1c\xeb\x0b\x01\x00\x06\x01=\x00\x00\x00\x02\x00\x00\x00\x03?\x00\x00\x00\x05\x00\x00\x00\x05D\x00\x00\x00\x06\x00\x00\x00\x07J\x00\x00\x00\x1d\x00\x00\x00\x08g\x00\x00\x00\x10\x00\x00\x00\tw\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00\x02\x06\x0c\n\x02\x00\x0cLibraAccount\x0frotate_base_url\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x04\x00\x0b\x00\x0b\x01\x11\x00\x02',
    "rotate_compliance_public_key": b'\xa1\x1c\xeb\x0b\x01\x00\x06\x01=\x00\x00\x00\x02\x00\x00\x00\x03?\x00\x00\x00\x05\x00\x00\x00\x05D\x00\x00\x00\x06\x00\x00\x00\x07J\x00\x00\x00*\x00\x00\x00\x08t\x00\x00\x00\x10\x00\x00\x00\t\x84\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00\x02\x06\x0c\n\x02\x00\x0cLibraAccount\x1crotate_compliance_public_key\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x04\x00\x0b\x00\x0b\x01\x11\x00\x02',
    "rotate_consensus_pubkey": b'\xa1\x1c\xeb\x0b\x01\x00\x06\x01=\x00\x00\x00\x06\x00\x00\x00\x03C\x00\x00\x00\x0f\x00\x00\x00\x05R\x00\x00\x00\x11\x00\x00\x00\x07c\x00\x00\x00Z\x00\x00\x00\x08\xbd\x00\x00\x00\x10\x00\x00\x00\t\xcd\x00\x00\x00\x14\x00\x00\x00\x00\x00\x00\x01\x00\x02\x01\x03\x00\x01\x00\x02\x04\x02\x03\x00\x00\x05\x00\x03\x00\x01\x06\x0c\x01\x05\x03\x06\x0c\x05\n\x02\x00\x02\x06\x0c\n\x02\x0bLibraSystem\x06Signer\x0fValidatorConfig\naddress_of\x14set_consensus_pubkey\x16update_and_reconfigure\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x03\x08\x00\n\x00\n\x00\x11\x00\x0b\x01\x11\x01\x0b\x00\x11\x02\x02',
    "rotate_shared_ed25519_public_key": b'\xa1\x1c\xeb\x0b\x01\x00\x06\x01=\x00\x00\x00\x02\x00\x00\x00\x03?\x00\x00\x00\x05\x00\x00\x00\x05D\x00\x00\x00\x06\x00\x00\x00\x07J\x00\x00\x00"\x00\x00\x00\x08l\x00\x00\x00\x10\x00\x00\x00\t|\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00\x02\x06\x0c\n\x02\x00\x16SharedEd25519PublicKey\nrotate_key\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x04\x00\x0b\x00\x0b\x01\x11\x00\x02',
    "rotate_validator_config": b'\xa1\x1c\xeb\x0b\x01\x00\x06\x01=\x00\x00\x00\x04\x00\x00\x00\x03A\x00\x00\x00\n\x00\x00\x00\x05K\x00\x00\x00\x12\x00\x00\x00\x07]\x00\x00\x00>\x00\x00\x00\x08\x9b\x00\x00\x00\x10\x00\x00\x00\t\xab\x00\x00\x00\x1a\x00\x00\x00\x00\x00\x00\x01\x01\x02\x00\x01\x00\x00\x03\x02\x01\x00\x07\x06\x0c\x05\n\x02\n\x02\n\x02\n\x02\n\x02\x00\x01\x06\x0c\x0bLibraSystem\x0fValidatorConfig\nset_config\x16update_and_reconfigure\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x0b\x00\n\x00\n\x01\x0b\x02\x0b\x03\x0b\x04\x0b\x05\x0b\x06\x11\x00\x0b\x00\x11\x01\x02',
    "tiered_mint": b'\xa1\x1c\xeb\x0b\x01\x00\x07\x01F\x00\x00\x00\x04\x00\x00\x00\x03J\x00\x00\x00\x0b\x00\x00\x00\x04U\x00\x00\x00\x02\x00\x00\x00\x05W\x00\x00\x00\x15\x00\x00\x00\x07l\x00\x00\x00J\x00\x00\x00\x08\xb6\x00\x00\x00\x10\x00\x00\x00\t\xc6\x00\x00\x00\x17\x00\x00\x00\x00\x00\x00\x01\x01\x02\x00\x01\x00\x00\x03\x02\x01\x01\x01\x01\x04\x02\x06\x0c\x03\x00\x04\x06\x0c\x05\x03\x03\x05\x06\x0c\x03\x05\x03\x03\x01\t\x00\x0cLibraAccount\x0cSlidingNonce\x15record_nonce_or_abort\x19mint_to_designated_dealer\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x03\x01\t\x00\n\x00\n\x01\x11\x00\x0b\x00\n\x02\n\x03\n\x048\x00\x02',
    "unfreeze_account": b'\xa1\x1c\xeb\x0b\x01\x00\x06\x01=\x00\x00\x00\x04\x00\x00\x00\x03A\x00\x00\x00\n\x00\x00\x00\x05K\x00\x00\x00\x0e\x00\x00\x00\x07Y\x00\x00\x00A\x00\x00\x00\x08\x9a\x00\x00\x00\x10\x00\x00\x00\t\xaa\x00\x00\x00\x12\x00\x00\x00\x00\x00\x00\x01\x01\x02\x00\x01\x00\x00\x03\x02\x01\x00\x02\x06\x0c\x03\x00\x02\x06\x0c\x05\x03\x06\x0c\x03\x05\x0cLibraAccount\x0cSlidingNonce\x15record_nonce_or_abort\x10unfreeze_account\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x01\x07\x00\n\x00\n\x01\x11\x00\x0b\x00\n\x02\x11\x01\x02',
    "unmint_lbr": b'\xa1\x1c\xeb\x0b\x01\x00\x08\x01O\x00\x00\x00\n\x00\x00\x00\x02Y\x00\x00\x00\x11\x00\x00\x00\x03j\x00\x00\x00\x11\x00\x00\x00\x04{\x00\x00\x00\x06\x00\x00\x00\x05\x81\x00\x00\x00?\x00\x00\x00\x07\xc0\x00\x00\x00E\x00\x00\x00\x08\x05\x01\x00\x00\x10\x00\x00\x00\t\x15\x01\x00\x00$\x00\x00\x00\x00\x00\x00\x01\x00\x02\x00\x03\x00\x04\x03\x05\x01\x01\x01\x00\x05\x02\x00\x01\x05\x02\x00\x02\x05\x01\x00\x02\x06\x00\x01\x00\x04\x07\x02\x03\x01\x01\x04\x08\x04\x05\x01\x01\x02\x07\x01\x08\x01\t\x02\x06\x0c\x0b\x00\x01\x08\x03\x02\x0b\x00\x01\x08\x01\x0b\x00\x01\x08\x02\x02\x06\x0c\x0b\x00\x01\t\x00\x00\x02\x06\x0c\x03\x01\x0b\x00\x01\t\x00\x03\x0b\x00\x01\x08\x01\x0b\x00\x01\x08\x02\x0b\x00\x01\x08\x03\x01\x08\x03\x01\x08\x01\x01\x08\x02\x05Coin1\x05Coin2\x03LBR\x05Libra\x0cLibraAccount\x01T\x06unpack\ndeposit_to\rwithdraw_from\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x06\x10\x00\n\x00\n\x018\x00\x0c\x04\n\x00\x0b\x04\x11\x00\x0c\x03\x0c\x02\n\x00\x0b\x028\x01\x0b\x00\x0b\x038\x02\x02',
    "update_exchange_rate": b'\xa1\x1c\xeb\x0b\x01\x00\x08\x01O\x00\x00\x00\x04\x00\x00\x00\x02S\x00\x00\x00\x04\x00\x00\x00\x03W\x00\x00\x00\x0b\x00\x00\x00\x04b\x00\x00\x00\x02\x00\x00\x00\x05d\x00\x00\x00\x14\x00\x00\x00\x07x\x00\x00\x00C\x00\x00\x00\x08\xbb\x00\x00\x00\x10\x00\x00\x00\t\xcb\x00\x00\x00\x15\x00\x00\x00\x00\x00\x00\x01\x00\x02\x02\x00\x00\x03\x00\x01\x00\x01\x04\x02\x03\x01\x01\x01\x05\x02\x03\x03\x01\x08\x00\x02\x06\x0c\x08\x00\x00\x03\x06\x0c\x03\x03\x01\t\x00\x0cFixedPoint32\x05Libra\x01T\x14create_from_rational\x18update_lbr_exchange_rate\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x04\x01\x08\x00\n\x01\n\x02\x11\x00\x0c\x03\x0b\x00\x0b\x038\x00\x02',
    "update_libra_version": b'\xa1\x1c\xeb\x0b\x01\x00\x06\x01=\x00\x00\x00\x02\x00\x00\x00\x03?\x00\x00\x00\x05\x00\x00\x00\x05D\x00\x00\x00\x05\x00\x00\x00\x07I\x00\x00\x00\x11\x00\x00\x00\x08Z\x00\x00\x00\x10\x00\x00\x00\tj\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00\x02\x06\x0c\x03\x00\x0cLibraVersion\x03set\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x04\x00\x0b\x00\n\x01\x11\x00\x02',
    "update_minting_ability": b'\xa1\x1c\xeb\x0b\x01\x00\x07\x01F\x00\x00\x00\x02\x00\x00\x00\x03H\x00\x00\x00\x06\x00\x00\x00\x04N\x00\x00\x00\x02\x00\x00\x00\x05P\x00\x00\x00\x08\x00\x00\x00\x07X\x00\x00\x00\x1d\x00\x00\x00\x08u\x00\x00\x00\x10\x00\x00\x00\t\x85\x00\x00\x00\r\x00\x00\x00\x00\x00\x00\x01\x00\x01\x01\x01\x00\x02\x02\x06\x0c\x01\x00\x01\t\x00\x05Libra\x16update_minting_ability\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x00\x01\x04\x00\x0b\x00\n\x018\x00\x02',
}

type_to_code_map = {
    CodeType.ADD_CURRENCY_TO_ACCOUNT: bytecodes["add_currency_to_account"],
    CodeType.ADD_VALIDATOR: bytecodes["add_validator"],
    CodeType.BURN: bytecodes["burn"],
    CodeType.BURN_TXN_FEES: bytecodes["burn_txn_fees"],
    CodeType.CANCEL_BURN: bytecodes["cancel_burn"],
    CodeType.CREATE_CHILD_VASP_ACCOUNT: bytecodes["create_child_vasp_account"],
    CodeType.CREATE_DESIGNATED_DEALER: bytecodes["create_designated_dealer"],
    CodeType.CREATE_PARENT_VASP_ACCOUNT: bytecodes["create_parent_vasp_account"],
    CodeType.CREATE_VALIDATOR_ACCOUNT: bytecodes["create_validator_account"],
    CodeType.EMPTY_SCRIPT: bytecodes["empty_script"],
    CodeType.FREEZE_ACCOUNT: bytecodes["freeze_account"],
    CodeType.MINT_LBR: bytecodes["mint_lbr"],
    CodeType.MINT_LBR_TO_ADDRESS: bytecodes["mint_lbr_to_address"],
    CodeType.MINT: bytecodes["mint"],
    CodeType.MODIFY_PUBLISHING_OPTION: bytecodes["modify_publishing_option"],
    CodeType.PEER_TO_PEER_WITH_METADATA: bytecodes["peer_to_peer_with_metadata"],
    CodeType.PREBURN: bytecodes["preburn"],
    CodeType.PUBLISH_SHARED_ED25519_PUBLIC_KEY: bytecodes["publish_shared_ed25519_public_key"],
    CodeType.REGISTER_PREBURNER: bytecodes["register_preburner"],
    CodeType.REGISTER_VALIDATOR: bytecodes["register_validator"],
    CodeType.REMOVE_ASSOCIATION_PRIVILEGE: bytecodes["remove_association_privilege"],
    CodeType.REMOVE_VALIDATOR: bytecodes["remove_validator"],
    CodeType.ROTATE_AUTHENTICATION_KEY: bytecodes["rotate_authentication_key"],
    CodeType.ROTATE_AUTHENTICATION_KEY_WITH_NONCE: bytecodes["rotate_authentication_key_with_nonce"],
    CodeType.ROTATE_BASE_URL: bytecodes["rotate_base_url"],
    CodeType.ROTATE_COMPLIANCE_PUBLIC_KEY: bytecodes["rotate_compliance_public_key"],
    CodeType.ROTATE_CONSENSUS_PUBKEY: bytecodes["rotate_consensus_pubkey"],
    CodeType.ROTATE_SHARED_ED25519_PUBLIC_KEY: bytecodes["rotate_shared_ed25519_public_key"],
    CodeType.ROTATE_VALIDATOR_CONFIG: bytecodes["rotate_validator_config"],
    CodeType.TIERED_MINT: bytecodes["tiered_mint"],
    CodeType.UNFREEZE_ACCOUNT: bytecodes["unfreeze_account"],
    CodeType.UNMINT_LBR: bytecodes["unmint_lbr"],
    CodeType.UPDATE_EXCHANGE_RATE: bytecodes["update_exchange_rate"],
    CodeType.UPDATE_LIBRA_VERSION: bytecodes["update_libra_version"],
    CodeType.UPDATE_MINTING_ABILITY: bytecodes["update_minting_ability"],
}

code_to_type_map = { v:k for k, v in type_to_code_map.items()}

import hashlib
def gen_hex_hash(code):
    m = hashlib.sha3_256()
    m.update(code)
    return m.hexdigest()

hash_to_type_map = { gen_hex_hash(v): k for k, v in type_to_code_map.items()}

default_currency_module_address = bytes.fromhex("7257c2417e4d1038e1817c8f283ace2e")

def get_code_type(code: bytes):
    if isinstance(code, str):
        code = bytes.fromhex(code)
    type = code_to_type_map.get(code)
    if type:
        return type
    return CodeType.UNKNOWN

def get_code(type, currency_module_address=None):
    code = type_to_code_map.get(type)
    if code:
        if currency_module_address:
            currency_module_address = AccountAddress.normalize_to_bytes(currency_module_address)
            code = code.replace(default_currency_module_address, currency_module_address)
        return code


def gen_code_type():
    for index, key in enumerate(bytecodes.keys()):
        print(f"{key.upper()} = {index}")

def gen_type_to_code_map():
    for key in bytecodes.keys():
        print(f'CodeType.{key.upper()}: bytecodes["{key}"],')


if __name__ == "__main__":
    gen_code_type()
    gen_type_to_code_map()



# def get_transaction_name(code):
#     for k, v in bytecodes.items():
#         if code == v:
#             return k+"_transaction"
#     return "unknown transaction"
#
# def get_code_by_jsonfile(script_file):
#     with open(script_file) as f:
#         amap = json.load(f)
#         return bytes(amap['code'])
#
# def get_code_by_filename(script_file):
#     with open(script_file, 'rb') as f:
#         code = f.read()
#         return code