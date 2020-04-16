from enum import IntEnum
from canoser import Struct
from libra.account_address import Address
from libra_client.client import LibraClient
from typing import Optional
from libra.waypoint import Waypoint
from libra.account_config import AccountConfig
from typing import Optional, Tuple, List, Union
from libra.account import Account
import os
from libra_client.wallet_library import Wallet
from libra.crypto.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from libra.transaction.transaction_payload import TransactionPayload
from libra.transaction.signed_transaction import SignedTransaction
from libra.transaction.raw_transaction import RawTransaction
from libra.transaction.authenticator import AuthenticationKey
from libra.rustlib import ensure
from libra.account_config import AccountConfig
from libra.transaction.script import Script
import requests
from json_rpc.views import AccountView
from libra.account import AccountStatus
import time
from error import ViolasError, StatusCode

CLIENT_WALLET_MNEMONIC_FILE = "client.mnemonic"
GAS_UNIT_PRICE = 0
MAX_GAS_AMOUNT = 400000
TX_EXPIRATION = 100

NETWORKS = {
    'libra_testnet':{
        'host': "ac.testnet.libra.org",
        'port': 8080,
        'faucet_server': "faucet.testnet.libra.org"
    },
    'violas_testnet':{
        "host": "52.27.228.84",
        "port": 50001,
        "faucet_file": "/root/violas_toml/mint.key"
    },
    'tianjin_testnet': {
        "host": "125.39.5.57",
        "port": 50001,
        "faucet_file": "/root/violas_toml/mint.key"
    },
    'local_testnet': {
        "host": "localhost",
        "port": 8000,
        "faucet_file": "/home/ops/config/mint.key"
    }

}

class Client():

    WAIT_TRANSACTION_COUNT = 1000
    WAIT_TRANSACTION_INTERVAL = 0.1
    def __init__(self, network="tianjin_testnet", waypoint: Optional[Waypoint]=None):
        ensure(network in NETWORKS, "The specified chain does not exist")
        chain = NETWORKS[network]
        ensure("host" in chain, "The specified chain has no host")
        ensure("port" in chain, "The specified chain has no port")
        url = f"http://{chain['host']}:{chain['port']}"
        self.client = LibraClient.new(url, waypoint)
        faucet_account_file = chain.get("faucet_file")
        if faucet_account_file is None:
            self.faucet_account = None
        else:
            self.faucet_account = Account.load_faucet_account_file(faucet_account_file)
        faucet_server = chain.get("faucet_server")
        self.faucet_server = faucet_server

    def get_balance(self, account_address: Union[bytes, str])-> Optional[int]:
        account_resource = self.get_account_resource(account_address)
        if account_resource:
            return account_resource.balance
        return 0

    def get_sequence_number(self, account_address: Union[bytes, str]) -> Optional[int]:
        account_resource = self.get_account_resource(account_address)
        if account_resource:
            return account_resource.sequence_number
        return 0

    def mint_coins(self, receiver_address, micro_coins, is_blocking=True, receiver_auth_key_prefix_opt=None):
        if self.faucet_account:
            script = Script.gen_mint_script(receiver_address, receiver_auth_key_prefix_opt, micro_coins)
            return self.association_transaction_with_local_faucet_account(script, is_blocking)
        ensure(receiver_auth_key_prefix_opt is not None, "Need authentication key to create new account via minting")
        receiver_auth_key = Address.normalize_to_bytes(receiver_auth_key_prefix_opt) + Address.normalize_to_bytes(receiver_address)
        return self.mint_coins_with_faucet_service(receiver_auth_key, micro_coins,  is_blocking)

    def enable_custom_script(self):
        pass

    def disable_custom_script(self):
        pass

    def remove_validator(self):
        pass

    def add_validator(self):
        pass

    def register_validator(self):
        pass

    def wait_for_transaction(self, address: Union[bytes, str], sequence_number: int):
        wait_time = 0
        while wait_time < self.WAIT_TRANSACTION_COUNT:
            time.sleep(self.WAIT_TRANSACTION_INTERVAL)
            transaction = self.get_account_transaction(address, sequence_number, fetch_events=False)
            if transaction is None:
                continue
            if transaction.is_successful():
                return
            raise ViolasError(transaction.get_vm_status())

        raise ViolasError(StatusCode.WAIT_TRANSACTION_TIME_OUT)


    def transfer_coins(self, sender_account: Account, micro_coins, receiver_address:Union[bytes, str], is_blocking=False, data:str=None,
            receiver_auth_key_prefix_opt:Optional[Union[bytes, str]]=None,
            gas_unit_price:int=GAS_UNIT_PRICE, max_gas_amount:int=MAX_GAS_AMOUNT):
        program = Script.gen_transfer_script(receiver_address, micro_coins, data, receiver_auth_key_prefix_opt)
        sequence_number = self.get_sequence_number(sender_account.address)
        txn = self.create_txn_to_submit(TransactionPayload("Script", program), sender_account, sequence_number, max_gas_amount, gas_unit_price)
        self.client.submit_transaction(txn)
        if is_blocking:
            self.wait_for_transaction(sender_account.address, sequence_number)
        return sequence_number

    def compile_program(self):
        pass

    def handle_dependencies(self):
        pass

    def submit_signed_transaction(self, signed_transaction: Union[bytes, str, SignedTransaction], is_blocking=True):
        if isinstance(signed_transaction, str):
            signed_transaction = bytes.fromhex(signed_transaction)
        if isinstance(signed_transaction, bytes):
            signed_transaction = SignedTransaction.deserialize(signed_transaction)
        sender_address = signed_transaction.sender
        sequence_number = signed_transaction.sequence_number
        self.client.submit_transaction(signed_transaction.deserialize())
        if is_blocking:
            self.wait_for_transaction(sender_address, sequence_number)
        return sequence_number


    def submit_program(self):
        pass

    def publish_module(self):
        pass

    def execute_script(self):
        pass

    def get_account_state(self, account_address: Union[bytes, str]):
        address = Address.normalize_to_bytes(account_address)
        account_state = self.client.get_account_state(address, True)
        return account_state

    def get_account_transaction(self, account_address: Union[bytes, str], sequence_number: int, fetch_events: bool=False):
        return self.client.get_txn_by_acc_seq(account_address, sequence_number, fetch_events)

    def get_transactions(self, start_version: int, limit: int, fetch_events: bool=True):
        return self.client.get_txn_by_range(start_version, limit, fetch_events)

    def get_sent_events(self, address):
        pass

    def get_received_events(self, address):
        pass

    def test_validator_connection(self):
        return self.client.get_metadata()

    def test_trusted_connection(self):
        return self.client.get_state_proof()

    def get_account_resource(self, address: Union[bytes, str]):
        account_state = self.get_account_state(address)
        return account_state[0].value

    def association_transaction_with_local_faucet_account(self, program, is_blocking):
        ensure(self.faucet_account is not None, "No faucet account loaded")
        sequence_number = self.get_sequence_number(self.faucet_account.address)
        txn = self.create_txn_to_submit(TransactionPayload("Script", program), self.faucet_account, sequence_number)
        self.client.submit_transaction(txn)
        if is_blocking:
            self.wait_for_transaction(self.faucet_account.address, sequence_number)
        return sequence_number

    def mint_coins_with_faucet_service(self, receiver: AuthenticationKey, micro_coins: int, is_blocking=True):
        ensure(self.faucet_server is not None, "Require faucet server")
        url = f"http://{self.faucet_server}?amount={micro_coins}&auth_key={receiver.hex()}"
        response = requests.post(url)
        body = response.text
        status = response.status_code
        ensure(status == requests.codes.ok, f"Failed to query remote faucet server[status={status}]: {body}")
        sequence_number = int(body)
        if is_blocking:
            self.wait_for_transaction(AccountConfig.association_address(), sequence_number-1)
        return sequence_number

    def create_txn_to_submit(self, payload: TransactionPayload, sender_account: Account, sequence_number, max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE) -> SignedTransaction:
        raw_tx = RawTransaction.new_tx(sender_account.address, sequence_number, payload, max_gas_amount, gas_unit_price)
        return SignedTransaction.gen_from_raw_txn(raw_tx, sender_account)



