from canoser import Struct, Uint64, BoolT, StrT, RustEnum

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

    @staticmethod
    def from_response(response):
        #TODO:
        return response.value.value

    def get_balance(self):
        return self.balance

    def get_sequence_number(self):
        return self.sequence_number

    def get_authentication_key(self):
        return self.authentication_key

    def get_sent_events_key(self):
        return self.sent_events_key

    def get_received_events_key(self):
        return self.received_events_key

    def get_delegated_key_rotation_capability(self):
        return self.delegated_key_rotation_capability

    def get_delegated_withdrawal_capability(self):
        return self.delegated_withdrawal_capability

class ReceivedPaymentEvent(Struct):
    _fields = [
        ("amount", Uint64),
        ("sender", StrT),
        ("metadata", StrT),
    ]

    def get_amount(self):
        return self.amount

    def get_sender(self):
        return self.sender

    def get_metadata(self):
        return self.metadata

class SentPaymentEvent(Struct):
    _fields = [
        ("amount", Uint64),
        ("receiver", StrT),
        ("metadata", StrT),
    ]

    def get_amount(self):
        return self.amount()

    def get_receiver(self):
        return self.receiver()

    def get_metadata(self):
        return self.metadata

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

    def get_key(self):
        return self.key

    def get_sequence_number(self):
        return self.sequence_number

    def get_transaction_version(self):
        return self.transaction_version

    def get_data(self):
        return self.data

    @classmethod
    def vec_from_response(cls, response):
        #TODO
        return response.value


class PeerToPeerScript(Struct):
    _fields = [
        ("receiver", StrT),
        ("auth_key_prefix", StrT),
        ("amount", Uint64),
        ("metadata", StrT),
    ]

    def get_receiver(self):
        return self.receiver

    def get_auth_key_prefix(self):
        return self.auth_key_prefix

    def get_amount(self):
        return self.amount

    def get_metadata(self):
        return self.metadata

class MintScript(Struct):
    _fields = [
        ("receiver", StrT),
        ("auth_key_prefix", StrT),
        ("amount", Uint64),
    ]

    def get_receiver(self):
        return self.receiver

    def get_auth_key_prefix(self):
        return self.auth_key_prefix

    def get_amount(self):
        return self.amount

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
        if type == "unknown_transaction":
            return cls("Unknown", UnknownScript())

    def get_receiver(self):
        if self.enum_name != "Unknown":
            return self.value.get_receiver()

    def get_amount(self):
        if self.enum_name != "Unknown":
            return self.value.get_amount()

    def get_metadata(self):
        if self.enum_name == "PeerToPeer":
            return self.value.get_metadata()


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

    def get_sender(self):
        return self.sender

    def get_signature_scheme(self):
        return self.signature_scheme

    def get_signature(self):
        return self.signature

    def get_public_key(self):
        return self.public_key

    def get_sequence_number(self):
        return self.sequence_number

    def get_max_gas_amount(self):
        return self.max_gas_amount

    def get_gas_unit_price(self):
        return self.gas_unit_price

    def get_expiration_time(self):
        return self.expiration_time

    def get_script_hash(self):
        return self.script_hash

    def get_script(self):
        return self.script

    def get_receiver(self):
        return self.script.get_receiver()

    def get_amount(self):
        return self.script.get_amount()

    def get_metadata(self):
        return self.script.get_metadata()

class BlockMetadataView(Struct):
    _fields = [
        ("version", Uint64),
        ("timestamp", Uint64)
    ]

    @classmethod
    def from_response(cls, response):
        return response.value

    def get_version(self):
        return self.version

    def get_timestamp(self):
        return self.timestamp

class BlockMetadata(Struct):
    _fields = [
        ("timestamp_usecs", Uint64)
    ]

    def get_timestamp_usecs(self):
        return self.timestamp_usecs

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

    def get_sender(self):
        if self.enum_name == "UserTransaction":
            return self.value.get_sender()

    def get_receiver(self):
        if self.enum_name == "UserTransaction":
            return self.value.get_receiver()

    def get_amount(self):
        if self.enum_name == "UserTransaction":
            return self.value.get_amount()

    def get_metadata(self):
        if self.enum_name == "UserTransaction":
            return self.value.get_metadata()

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

    def get_sender(self):
        return self.transaction.get_sender()

    def get_receiver(self):
        return self.transaction.get_receiver()

    def get_amount(self):
        return self.transaction.get_amount()

    def get_metadata(self):
        return self.transaction.get_metadata()

class StateProofView(Struct):
    _fields = [
        ("ledger_info_with_signatures", StrT),
        ("validator_change_proof", StrT),
        ("ledger_consistency_proof", StrT),
    ]

    @staticmethod
    def from_response(response):
        return response.value

class AccountStateWithProofView(Struct):

    def from_response(self, response):
        return response.value