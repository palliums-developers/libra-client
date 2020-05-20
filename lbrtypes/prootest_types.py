from canoser import Struct, Uint64
from lbrtypes.account_address import AccountAddress
from crypto.ed25519 import Ed25519PublicKey, Ed25519PrivateKey
from lbrtypes.event import EventHandle
from lbrtypes.identifier import Identifier
from lbrtypes.transaction import Version
from lbrtypes.block_info import Round
from lbrtypes.transaction import TransactionPayload

class AccountInfo(Struct):
    _fields = [
        ("address", AccountAddress),
        ("private_key", Ed25519PrivateKey),
        ("public_key", Ed25519PublicKey),
        ("sequence_number", Uint64),
        ("sent_event_handle", EventHandle),
        ("received_event_handle", EventHandle),
        ("balance_currency_code", Identifier),
    ]


class AccountInfoUniverse(Struct):
    _fields = [
        ("accounts", [AccountInfo]),
        ("epoch", Uint64),
        ("round", Round),
        ("next_version", Version),
    ]

class RawTransactionGen(Struct):
    _fields = [
        ("payload", TransactionPayload),
        ("max_gas_amount", Uint64),
        ("gas_unit_price", Uint64),
        ("expiration_time_secs", Uint64),
    ]

class SignatureCheckedTransactionGen(Struct):
    _fields = [
        ("raw_transaction_gen", RawTransactionGen)
    ]