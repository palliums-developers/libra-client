import requests
import json

from json_rpc.client import JsonRpcBatch, process_batch_response
from libra.rustlib import ensure
from error import ViolasError, StatusCode
from libra.waypoint import Waypoint
from typing import Optional, Union
from libra.trusted_state import TrustedState
from libra.ledger_info import LedgerInfoWithSignatures
from libra.transaction import SignedTransaction
from json_rpc.client import get_response_from_batch, JsonRpcResponse
from json_rpc.views import AccountView, EventView, BlockMetadataView, TransactionView, TransactionDataView, StateProofView, AccountStateWithProofView
from libra.account_state_blob import AccountStateBlob
from libra.access_path import AccessPath
from libra.account_config import AccountConfig
from libra.account import Account

JSON_RPC_TIMEOUT_MS = 50000
MAX_JSON_RPC_RETRY_COUNT = 2

class JsonRpcClient():
    def __init__(self, url):
        self.url = url

    @classmethod
    def new(cls, url):
        return cls(url)

    def execute(self, batch: JsonRpcBatch):
        if len(batch.requests) == 0:
            return list()
        request = batch.json_request()
        response = self.send_with_retry(request)
        if response.status_code != 200:
            raise ViolasError(StatusCode.FETCH_ERROR_MESSAGE, f"Server returned error: {response.status_code}")
        response = process_batch_response(batch, response.json())
        ensure(len(batch.requests) == len(response), "received unexpected number of responses in batch")
        return response

    def send_with_retry(self, request):
        response = self.send(request)
        try_cnt = 0
        while try_cnt < MAX_JSON_RPC_RETRY_COUNT and response.status_code != 200:
            response = self.send(request)
            try_cnt += 1
        return response

    def send(self,request):
        headers = {'content-type': 'application/json'}
        return requests.post(self.url, data=json.dumps(request),headers=headers, timeout=JSON_RPC_TIMEOUT_MS)


class LibraClient():
    def __init__(self, client: JsonRpcClient, trusted_state: TrustedState, latest_epoch_change_li: Optional[LedgerInfoWithSignatures]):
        self.client = client
        self.trusted_state = trusted_state
        self.latest_epoch_change_li = latest_epoch_change_li

    @classmethod
    def new(cls, url, waypoint: Optional[Waypoint]):
        if waypoint is None:
            initial_trusted_state = TrustedState.new_trust_any_genesis_WARNING_UNSAFE()
        else:
            initial_trusted_state = TrustedState.from_waypoint(waypoint)
        client = JsonRpcClient(url)
        return cls(client, initial_trusted_state, None)


    def submit_transaction(self, transaction: SignedTransaction):
        batch = JsonRpcBatch.new()
        batch.add_submit_request(transaction)
        response = self.client.execute(batch)
        response = get_response_from_batch(0, response)
        self._handle_response(response)


    def get_account_state(self, account: bytes, with_state_proof: bool)-> AccountView:
        client_version = self.trusted_state.latest_version
        batch = JsonRpcBatch.new()
        batch.add_get_account_state_request(account)
        if with_state_proof:
            batch.add_get_state_proof_request(client_version)
        responses = self.client.execute(batch)
        if with_state_proof:
            state_proof = get_response_from_batch(1, responses)
            self.process_state_proof_response(state_proof)
        response = get_response_from_batch(0, responses)
        ensure(isinstance(response, JsonRpcResponse), f"Failed to get account state for account address {account} with error: {response}")
        account_view = AccountView.from_response(response)
        return account_view

    def get_events(self, event_key, start: int, limit: int) -> EventView:
        batch = JsonRpcBatch.new()
        batch.add_get_events_request(event_key, start, limit)
        responses = self.client.execute(batch)
        response = get_response_from_batch(0, responses)
        ensure(isinstance(response, JsonRpcResponse), f"Failed to get events with error: {response}")
        return EventView.vec_from_response(response)

    def get_metadata(self):
        batch = JsonRpcBatch.new()
        batch.add_get_metadata_request()
        response = self.client.execute(batch)
        response = get_response_from_batch(0, response)
        self._handle_response(response)
        return BlockMetadataView.from_response(response)

    def get_state_proof(self):
        batch = JsonRpcBatch.new()
        batch.add_get_state_proof_request(self.trusted_state.latest_version)
        responses = self.client.execute(batch)
        state_proof = get_response_from_batch(0, responses)
        return self.process_state_proof_response(state_proof)

    def process_state_proof_response(self, response):
        ensure(isinstance(response, JsonRpcResponse), f"Failed to get state proof with error: {response}")
        state_proof = StateProofView.from_response(response)
        return state_proof
        #TODO
        # return self.verify_state_proof(state_proof)

    def verify_state_proof(self, state_proof: StateProofView):
        pass

    def get_account_blob(self, address: bytes):
        version = self.trusted_state.latest_version
        batch = JsonRpcBatch.new()
        batch.add_get_account_state_with_proof_request(address, version, version)
        responses = self.client.execute(batch)
        response = get_response_from_batch(0, responses)
        ensure(isinstance(response, JsonRpcResponse), f"Failed to get account state blob with error: {response}")
        account_state_with_proof = AccountStateWithProofView.from_response(response)
        blob = account_state_with_proof.blob
        if blob:
            account_blob = AccountStateBlob.deserialize(blob)
            return account_blob

    def get_txn_by_acc_seq(self, account: bytes, sequence_number: int, fetch_events: bool):
        batch = JsonRpcBatch.new()
        batch.add_get_account_transaction_request(account, sequence_number, fetch_events)
        batch.add_get_state_proof_request(self.trusted_state.latest_version)
        responses = self.client.execute(batch)
        state_proof_view = get_response_from_batch(1, responses)
        self.process_state_proof_response(state_proof_view)
        response = get_response_from_batch(0, responses)
        self._handle_response(response)
        return TransactionView.from_response(response)

    def get_txn_by_range(self, start_version: int, limit: int, fetch_events: bool):
        batch = JsonRpcBatch.new()
        batch.add_get_transactions_request(start_version, limit, fetch_events)
        batch.add_get_state_proof_request(self.trusted_state.latest_version)
        responses = self.client.execute(batch)
        state_proof = get_response_from_batch(1, responses)
        self.process_state_proof_response(state_proof)
        response = get_response_from_batch(0, responses)
        self._handle_response(response)
        return TransactionView.vec_from_response(response)

    def get_sequence_number(self, account: bytes):
        state, _ = self.get_account_state(account, True)
        if state:
            return state.sequence_number

    def get_events_by_access_path(self, access_path: AccessPath, start_event_seq_num: int, limit: int):
        account_view = self.get_account_state(access_path.address, False)
        if account_view is None:
            return []
        path = access_path.path
        ensure(path in (AccountConfig.account_sent_event_path(), AccountConfig.account_received_event_path()), "Unexpected event path found in access path")
        if path == AccountConfig.account_sent_event_path():
            event_key = account_view.sent_events_key
        elif path == AccountConfig.account_received_event_path():
            event_key = account_view.received_events_key
        events = self.get_events(event_key, start_event_seq_num, limit)
        return events

    def _handle_response(self, response):
        if isinstance(response, dict):
            raise ViolasError.from_response(response)










