from canoser import Struct, Uint64, BoolT, StrT, RustEnum
from libra.account_resource import AccountResource, BalanceResource
from libra.rustlib import ensure
from libra.vm_error import StatusCode

class AccountView(Struct):
    _fields = [
        ("balance", Uint64),
        ("sequence_number", Uint64),
        ("authentication_key", StrT),
        ("sent_events_key", StrT),
        ("received_events_key", StrT),
        ("delegated_key_rotation_capability", BoolT),
        ("delegated_withdrawal_capability", BoolT),
    ]

    @classmethod
    def from_value(cls, value):
        ret = cls()
        ret.balance = value.get("balance")
        ret.sequence_number = value.get("sequence_number")
        ret.authentication_key = value.get("authentication_key")
        ret.sent_events_key = value.get("sent_events_key")
        ret.received_events_key = value.get("received_events_key")
        ret.delegated_key_rotation_capability = value.get("delegated_key_rotation_capability")
        ret.delegated_withdrawal_capability = value.get("delegated_withdrawal_capability")
        return ret

    @classmethod
    def new(cls, account: AccountResource, balance: BalanceResource):
        ret = cls()
        ret.balance = account.balance.coin
        ret.sequence_number = account.sequence_number
        ret.authentication_key = account.authentication_key
        ret.sent_events_key = account.sent_events.key
        ret.received_events_key = account.received_events.key
        ret.delegated_key_rotation_capability = account.delegated_key_rotation_capability
        ret.delegated_withdrawal_capability = account.delegated_withdrawal_capability

    @staticmethod
    def optional_from_response(response):
        #TODO:
        return response.value


class ReceivedPaymentEvent(Struct):
    _fields = [
        ("amount", Uint64),
        ("sender", StrT),
        ("metadata", StrT),
    ]

class SentPaymentEvent(Struct):
    _fields = [
        ("amount", Uint64),
        ("receiver", StrT),
        ("metadata", StrT),
    ]

class EventDataView(RustEnum):
    _enums = [
        ("ReceivedPayment", ReceivedPaymentEvent),
        ("SentPayment", SentPaymentEvent),
        ("Unknown", None)
    ]

    @classmethod
    def from_value(cls, value):
        if value["type"] == "sentpayment":
            return cls("SentPayment", SentPaymentEvent.from_value(value))
        if value["type"] == "receivedpayment":
            return cls("ReceivedPayment", ReceivedPaymentEvent.from_value(value))
        if value["type"] == "unknown":
            return cls("Unknown", None)

class EventView(Struct):
    _fields = [
        ("key", StrT),
        ("sequence_number", Uint64),
        ("transaction_version", Uint64),
        ("data", EventDataView),

    ]
    def vec_from_response(self, response):
        #TODO
        return response.value


class PeerToPeerScript(Struct):
    _fields = [
        ("receiver", StrT),
        ("auth_key_prefix", StrT),
        ("amount", Uint64),
        ("metadata", StrT),
    ]

class MintScript(Struct):
    _fields = [
        ("receiver", StrT),
        ("auth_key_prefix", StrT),
        ("amount", Uint64),
    ]

class UnknownScript(Struct):
    _fields = [
    ]


class ScriptView(RustEnum):
    _enums = [
        ("PeerToPeer", PeerToPeerScript),
        ("Mint", MintScript),
        ("Unknown", UnknownScript)
    ]

    @classmethod
    def from_value(cls, value):
        type = value.get("type")
        if type == "mint_transaction":
            return cls("Mint", MintScript.from_value(value))
        if type == "peer_to_peer_transaction":
            return cls("PeerToPeer", PeerToPeerScript.from_value(value))


class UserTransaction(Struct):
    _fields = [
        ("sender", StrT),
        ("signature_scheme", StrT),
        ("signature", StrT),
        ("public_key", StrT),
        ("sequence_number", Uint64),
        ("max_gas_amount", Uint64),
        ("gas_unit_price", Uint64),
        ("expiration_time", Uint64),
        ("script_hash", StrT),
        ("script", ScriptView)
    ]

class BlockMetadata(Struct):
    _fields = [
        ("timestamp_usecs", Uint64)
    ]

class TransactionDataView(RustEnum):
    _enums = [
        ("BlockMetadata", BlockMetadata),
        ("WriteSet", None),
        ("UserTransaction", UserTransaction),
        ("UnknownTransaction", None)
    ]

    @classmethod
    def from_value(cls, value):
        if value.get("type") == "user":
            return cls("UserTransaction", UserTransaction.from_value(value))
        if value.get("type") == "blockmetadata":
            return cls("BlockMetadata", BlockMetadata.from_value(value))
        if value.get("type") == "writeset":
            return cls("WriteSet", None)

class TransactionView(Struct):
    _fields = [
        ("version", Uint64),
        ("transaction", TransactionDataView),
        ("events", [EventView]),
        ("vm_status", Uint64),
        ("gas_used", Uint64)
    ]

    @classmethod
    def from_response(cls, response):
        return response.value.value

    @classmethod
    def vec_from_response(cls, response):
        return response.value

    def is_successful(self) -> bool:
        return self.vm_status == 4001

    def get_version(self) -> int:
        return self.version

    def get_transaction_data(self) -> TransactionDataView:
        return self.transaction

    from typing import List
    def get_events(self) -> List[EventView]:
        return self.events

    def get_vm_status(self) -> int:
        return self.vm_status

    def get_gas_used(self) -> int:
        return self.gas_used


class StateProofView(Struct):
    _fields = [
        ("ledger_info_with_signatures", StrT),
        ("validator_change_proof", StrT),
        ("ledger_consistency_proof", StrT),
    ]

    @staticmethod
    def from_response(response):
        return response.value

class AccountStateWithProofView():
    def from_response(self, response):
        return response.value