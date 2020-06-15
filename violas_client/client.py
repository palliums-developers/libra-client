import time
import requests
from json_rpc.views import TransactionView
from typing import Optional, Union

from lbrtypes.move_core.account_address import AccountAddress as Address
from libra_client.methods import LibraClient
from lbrtypes.waypoint import Waypoint
from .account import Account
from lbrtypes.transaction import TransactionPayload, SignedTransaction
from lbrtypes.transaction.script import Script
from lbrtypes.rustlib import ensure
from lbrtypes.access_path import AccessPath
from error import LibraError, StatusCode, ServerCode
from lbrtypes.bytecode import CodeType
from lbrtypes.transaction.transaction_argument import TransactionArgument
from lbrtypes.account_config import get_coin_type, ACCOUNT_SENT_EVENT_PATH, ACCOUNT_RECEIVED_EVENT_PATH, association_address, config_address
from lbrtypes.transaction.helper import create_user_txn
from lbrtypes.account_state import AccountState

import os
pre_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../key'))

CLIENT_WALLET_MNEMONIC_FILE = "client.mnemonic"
GAS_UNIT_PRICE = 0
MAX_GAS_AMOUNT = 1_000_000
TX_EXPIRATION = 100

NETWORKS = {
    'libra_testnet':{
        "url": "https://client.testnet.lbrtypes.org",
        'faucet_server': "faucet.testnet.lbrtypes.org"
    },
    'violas_testnet':{
        "url": "http://52.27.228.84:50001",
        "faucet_file": f"{pre_path}/mint_test.key"
    },
    'tianjin_testnet': {
        "url": "http://125.39.5.57:50001",
        "faucet_file": "/root/key/mint_tianjin.key"
    },

    'bj_testnet': {
        "url": "http://47.93.114.230:46659",
        "faucet_file": f"{pre_path}/mint_bj.key"
    }
}

class Client():
    GRPC_TIMEOUT = 30
    MAX_GAS_AMOUNT = 1_000_000
    GAS_UNIT_PRICE = 0
    TXN_EXPIRATION = 100
    RECONNECT_COUNT = 2

    WAIT_TRANSACTION_COUNT = 1000
    WAIT_TRANSACTION_INTERVAL = 0.1
    def __init__(self, network="violas_testnet", waypoint: Optional[Waypoint]=None):
        ensure(network in NETWORKS, "The specified chain does not exist")
        chain = NETWORKS[network]
        ensure("url" in chain, "The specified chain has no url")
        url = chain.get("url")
        self.client = LibraClient.new(url, waypoint)
        faucet_account_file = chain.get("faucet_file")
        if faucet_account_file is None:
            self.faucet_account = None
        else:
            self.faucet_account = Account.load_faucet_account_file(faucet_account_file)
        faucet_server = chain.get("faucet_server")
        self.faucet_server = faucet_server

    @classmethod
    def new(cls, url, faucet_file:Optional[str]=None, faucet_server:Optional[str]=None, waypoint:Optional[Waypoint]=None):
        ret = cls.__new__(cls)
        ret.client = LibraClient.new(url, waypoint)
        faucet_account_file = faucet_file
        if faucet_account_file is None:
            ret.faucet_account = None
        else:
            ret.faucet_account = Account.load_faucet_account_file(faucet_account_file)
        faucet_server = faucet_server
        ret.faucet_server = faucet_server
        return ret

    def get_balance(self, account_address: Union[bytes, str], currency_code=None, currency_module_address=None)-> Optional[int]:
        account_state = self.get_account_state(account_address)
        if account_state:
            return account_state.get_balance(currency_module_address, currency_code)
        return 0

    def get_balances(self, account_address: Union[bytes, str]):
        address = Address.normalize_to_bytes(account_address)
        state = self.client.get_account_state(address, True)
        if state:
            return { balance.currency: balance.amount for balance in state.balances}
        return {}

    def get_sequence_number(self, account_address: Union[bytes, str]) -> Optional[int]:
        account_state = self.get_account_blob(account_address)
        if account_state:
            return account_state.get_sequence_number()
        return 0

    def get_latest_version(self):
        metadata = self.get_metadata()
        return metadata.version

    def get_registered_currencies(self):
        from lbrtypes.account_config import config_address
        state = self.get_account_state(config_address())
        return state.get_registered_currencies()

    def get_account_state(self, account_address: Union[bytes, str]) -> Optional[AccountState]:
        return self.get_account_blob(account_address)
        # address = Address.normalize_to_bytes(account_address)
        # return self.client.get_account_state(address, True)

    def get_account_blob(self, account_address: Union[bytes, str]):
        address = Address.normalize_to_bytes(account_address)
        return self.client.get_account_blob(address)

    def get_account_transaction(self, account_address: Union[bytes, str], sequence_number: int, fetch_events: bool=True) -> TransactionView:
        return self.client.get_txn_by_acc_seq(account_address, sequence_number, fetch_events)

    def get_transactions(self, start_version: int, limit: int, fetch_events: bool=True) -> [TransactionView]:
        try:
            return self.client.get_txn_by_range(start_version, limit, fetch_events)
        except LibraError as e:
            return []

    def get_transaction(self, version, fetch_events:bool=True):
        txs = self.get_transactions(version, 1, fetch_events)
        if len(txs) == 1:
            return txs[0]

    def get_sent_events(self, address: Union[bytes, str], start: int, limit: int):
        address = Address.normalize_to_bytes(address)
        path = ACCOUNT_SENT_EVENT_PATH
        access_path = AccessPath(address, path)
        return self.client.get_events_by_access_path(access_path, start, limit)

    def get_received_events(self, address: Union[bytes, str], start: int, limit: int):
        address = Address.normalize_to_bytes(address)
        path = ACCOUNT_RECEIVED_EVENT_PATH
        access_path = AccessPath(address, path)
        return self.client.get_events_by_access_path(access_path, start, limit)

    def get_metadata(self):
        return self.client.get_metadata()

    def get_state_proof(self):
        return self.client.get_state_proof()

    def get_type_args(self, currency_module_address, currency_code, struct_name=None):
        coin_type = get_coin_type(currency_module_address, currency_code, struct_name)
        if coin_type:
            return [coin_type]
        return []

    def require_faucet_account(self):
        ensure(self.faucet_account is not None, "facucet_account is not set")

    def add_currency_to_account(self, sender_account, currency_code, currency_module_address=None, is_blocking=True,
            max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE,txn_expiration=TXN_EXPIRATION):
        args = []
        ty_args = self.get_type_args(currency_module_address, currency_code)
        script = Script.gen_script(CodeType.ADD_CURRENCY_TO_ACCOUNT, *args, ty_args=ty_args,
                                   currency_module_address=currency_module_address)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount=max_gas_amount, gas_unit_price=gas_unit_price, txn_expiration=txn_expiration)

    def mint_coin(self, receiver_address, micro_coins, auth_key_prefix=None, is_blocking=True, currency_module_address=None,
                  currency_code=None,
                  max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE, txn_expiration=TXN_EXPIRATION):
        from lbrtypes.account_config import LBR_NAME
        if self.faucet_account:
            args = []
            args.append(TransactionArgument.to_address(receiver_address))
            args.append(TransactionArgument.to_U8Vector(auth_key_prefix))
            args.append(TransactionArgument.to_U64(micro_coins))
            if currency_code in (None, LBR_NAME):
                script = Script.gen_script(CodeType.MINT_LBR_TO_ADDRESS, *args, currency_module_address=currency_module_address)
            else:
                ty_args = self.get_type_args(currency_module_address, currency_code)
                script = Script.gen_script(CodeType.MINT, *args, ty_args=ty_args, currency_module_address=currency_module_address)

            return self.submit_script(self.faucet_account, script, is_blocking, "LBR", max_gas_amount, gas_unit_price,
                                      txn_expiration)
        else:
            return self.mint_coin_with_faucet_service(receiver_address, micro_coins, is_blocking)

    def mint_coin_with_faucet_service(self, receiver, micro_coins: int, is_blocking=True):
        ensure(self.faucet_server is not None, "Require faucet server")
        url = f"http://{self.faucet_server}?amount={micro_coins}&auth_key={receiver.hex()}"
        response = requests.post(url)
        body = response.text
        status = response.status_code
        ensure(status == requests.codes.ok, f"Failed to query remote faucet server[status={status}]: {body}")
        sequence_number = int(body)
        if is_blocking:
            self.wait_for_transaction(association_address(), sequence_number - 1)
        return sequence_number

    def transfer_coin(self, sender_account, receiver_address, micro_coins, currency_module_address=None,
                      currency_code=None, is_blocking=True, data=None,
                      gas_currency_code=None, max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE, txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_address(receiver_address))
        args.append(TransactionArgument.to_U64(micro_coins))
        args.append(TransactionArgument.to_U8Vector(data, hex=False))
        args.append(TransactionArgument.to_U8Vector(""))

        ty_args = self.get_type_args(currency_module_address, currency_code)
        script = Script.gen_script(CodeType.PEER_TO_PEER_WITH_METADATA, *args, ty_args=ty_args, currency_module_address=currency_module_address)
        return self.submit_script(sender_account, script, is_blocking,self.get_gas_currency_code(currency_code, gas_currency_code), max_gas_amount, gas_unit_price, txn_expiration)


    '''Called by the object'''
    def wait_for_transaction(self, address: Union[bytes, str], sequence_number: int):
        wait_time = 0
        while wait_time < self.WAIT_TRANSACTION_COUNT:
            wait_time += 1
            time.sleep(self.WAIT_TRANSACTION_INTERVAL)
            transaction = self.get_account_transaction(address, sequence_number, fetch_events=False)
            if transaction is None:
                continue
            if transaction.is_successful():
                return
            raise LibraError(ServerCode.VmStatusError, transaction.get_vm_status())

        raise LibraError(ServerCode.VmStatusError, StatusCode.WAIT_TRANSACTION_TIME_OUT)

    def submit_signed_transaction(self, signed_transaction: Union[bytes, str, SignedTransaction], is_blocking=True):
        if isinstance(signed_transaction, str):
            signed_transaction = bytes.fromhex(signed_transaction)
        if isinstance(signed_transaction, bytes):
            signed_transaction = SignedTransaction.deserialize(signed_transaction)
        sender_address = signed_transaction.get_sender()
        sequence_number = signed_transaction.get_sequence_number()
        self.client.submit_transaction(signed_transaction)
        if is_blocking:
            self.wait_for_transaction(sender_address, sequence_number)
        return sequence_number

    def submit_script(self, sender_account, script, is_blocking=True, gas_currency_code=None, max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE, txn_expiration=TXN_EXPIRATION):
        gas_currency_code = self.get_gas_currency_code(gas_currency_code=gas_currency_code)
        sequence_number = self.get_sequence_number(sender_account.address)
        signed_txn = create_user_txn(TransactionPayload("Script",script), sender_account, sequence_number, max_gas_amount, gas_unit_price, gas_currency_code, txn_expiration)
        self.submit_signed_transaction(signed_txn, is_blocking)
        return sequence_number

    def submit_module(self, sender_account, module,  is_blocking=True, gas_currency_code=None, max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE, txn_expiration=TXN_EXPIRATION):
        gas_currency_code = self.get_gas_currency_code(gas_currency_code=gas_currency_code)
        sequence_number = self.get_sequence_number(sender_account.address)
        signed_txn = create_user_txn(TransactionPayload("Module", module), sender_account, sequence_number, max_gas_amount, gas_unit_price, gas_currency_code, txn_expiration)
        self.submit_signed_transaction(signed_txn, is_blocking)
        return sequence_number

    def get_gas_currency_code(self, currency_code=None, gas_currency_code=None):
        if gas_currency_code:
            return gas_currency_code
        if currency_code:
            return currency_code
        from lbrtypes.account_config import LBR_NAME
        return LBR_NAME
