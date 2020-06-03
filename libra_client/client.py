import time
import requests
from json_rpc.views import TransactionView
from typing import Optional, Union

from lbrtypes.move_core.account_address import AccountAddress as Address
from libra_client.methods import LibraClient
from lbrtypes.waypoint import Waypoint
from libra_client.account import Account
from lbrtypes.transaction import TransactionPayload, SignedTransaction
from lbrtypes.transaction.script import Script
from lbrtypes.rustlib import ensure
from lbrtypes.access_path import AccessPath
from error import LibraError, StatusCode, ServerCode
from lbrtypes.bytecode import CodeType
from lbrtypes.transaction.transaction_argument import TransactionArgument
from lbrtypes.account_config import get_coin_type, ACCOUNT_SENT_EVENT_PATH, ACCOUNT_RECEIVED_EVENT_PATH, association_address
from lbrtypes.transaction.helper import create_user_txn
from lbrtypes.transaction.module import Module
from lbrtypes.account_state import AccountState

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
        "host": "125.39.5.57",
        "faucet_file": "/root/palliums/violas_toml/mint.key"
    },
    'tianjin_testnet': {
        "url": "http://125.39.5.57:50001",
        "host": "125.39.5.57",
        "faucet_file": "/root/palliums/violas_toml/mint_tianjin.key"
    },

    'bj_testnet': {
        "url": "http://47.93.114.230:50001",
        "host": "47.93.114.230",
        "faucet_file": "/root/palliums/violas_toml/mint_bj.key"
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
    def __init__(self, network="tianjin_testnet", waypoint: Optional[Waypoint]=None):
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

    def get_sequence_number(self, account_address: Union[bytes, str]) -> Optional[int]:
        account_state = self.get_account_blob(account_address)
        if account_state:
            return account_state.get_sequence_number()
        return 0

    def get_account_state(self, account_address: Union[bytes, str]) -> Optional[AccountState]:
        return self.get_account_blob(account_address)
        # address = Address.normalize_to_bytes(account_address)
        # return self.client.get_account_state(address, True)

    def get_account_blob(self, account_address: Union[bytes, str]):
        address = Address.normalize_to_bytes(account_address)
        return self.client.get_account_blob(address)

    def get_account_transaction(self, account_address: Union[bytes, str], sequence_number: int, fetch_events: bool=False) -> TransactionView:
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

    def get_latest_version(self):
        metadata = self.get_metadata()
        return metadata.version

    def get_registered_currencies(self):
        from lbrtypes.account_config import config_address
        state = self.get_account_state(config_address())
        return state.get_registered_currencies()

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

    def add_validator(self, validator_address, is_blocking=True,
                      gas_currency_code=None, max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE, txn_expiration=TXN_EXPIRATION):
        self.require_faucet_account()
        args = []
        args.append(TransactionArgument.to_address(validator_address))

        script = Script.gen_script(CodeType.ADD_VALIDATOR, *args)
        return self.submit_script(self.faucet_account, script, is_blocking, max_gas_amount, gas_unit_price,
                                  txn_expiration)

    def allow_child_accounts(self, sender_account, is_blocking=True,
                             max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE,
                             txn_expiration=TXN_EXPIRATION):
        args = []

        script = Script.gen_script(CodeType.ALLOW_CHILD_ACCOUNTS, *args)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def apply_for_association_address(self, sender_account, is_blocking=True,
                                      max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE,
                                      txn_expiration=TXN_EXPIRATION):
        args = []

        script = Script.gen_script(CodeType.APPLY_FOR_ASSOCIATION_ADDRESS, *args)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def apply_for_association_privilege(self, sender_account, is_blocking=True,
                                        max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE,
                                        txn_expiration=TXN_EXPIRATION):
        args = []
        script = Script.gen_script(CodeType.APPLY_FOR_ASSOCIATION_ADDRESS, *args)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def apply_for_child_vasp_credential(self, sender_account, root_vasp_address, is_blocking=True,
                                        max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE,
                                        txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_address(root_vasp_address))

        script = Script.gen_script(CodeType.APPLY_FOR_CHILD_VASP_CREDENTIAL, *args)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def apply_for_parent_capability(self, sender_account, is_blocking=True,
                                    max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE,
                                    txn_expiration=TXN_EXPIRATION):
        args = []

        script = Script.gen_script(CodeType.APPLY_FOR_PARENT_CAPABILITY, *args)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def apply_for_root_vasp(self, sender_account, human_name, base_url, ca_cert, travel_rule_public_key,
                            is_blocking=True,
                            max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE,
                            txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_U8Vector(human_name, hex=False))
        args.append(TransactionArgument.to_U8Vector(base_url, hex=False))
        args.append(TransactionArgument.to_U8Vector(ca_cert))
        args.append(TransactionArgument.to_U8Vector(travel_rule_public_key))

        script = Script.gen_script(CodeType.APPLY_FOR_ROOT_VASP, *args)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def approved_payment(self, sender_account, receiver_address, amount, metadata, signature, currency_module_address=None,
                         currency_code=None, is_blocking=True,
                         gas_currency_code=None, max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE, txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_address(receiver_address))
        args.append(TransactionArgument.to_U8Vector(amount))
        args.append(TransactionArgument.to_U8Vector(metadata))
        args.append(TransactionArgument.to_U8Vector(signature))

        ty_args = self.get_type_args(currency_module_address, currency_code)
        script = Script.gen_script(CodeType.APPROVED_PAYMENT, *args, ty_args=ty_args, currency_module_address=currency_module_address)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def burn(self, sender_account, preburn_address, currency_module_address=None, currency_code=None, is_blocking=True,
             gas_currency_code=None, max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE, txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_address(preburn_address))

        ty_args = self.get_type_args(currency_module_address, currency_code)
        script = Script.gen_script(CodeType.BURN, *args, ty_args=ty_args, currency_module_address=currency_module_address)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def cancel_burn(self, sender_account, preburn_address, currency_module_address=None, currency_code=None, is_blocking=True,
                    gas_currency_code=None, max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE, txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_address(preburn_address))

        ty_args = self.get_type_args(currency_module_address, currency_code)
        script = Script.gen_script(CodeType.CANCEL_BURN, *args, ty_args=ty_args, currency_module_address=currency_module_address)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def create_account(self, sender_account, fresh_address, auth_key_prefix, initial_amount=0, currency_module_address=None,
                       currency_code=None, is_blocking=True,
                       gas_currency_code=None, max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE, txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_address(fresh_address))
        args.append(TransactionArgument.to_U8Vector(auth_key_prefix))
        args.append(TransactionArgument.to_U64(initial_amount))

        ty_args = self.get_type_args(currency_module_address, currency_code)
        script = Script.gen_script(CodeType.CREATE_ACCOUNT, *args, ty_args=ty_args, currency_module_address=currency_module_address)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def create_empty_account(self, sender_account, fresh_address, auth_key_prefix, currency_module_address=None,
                             currency_code=None, is_blocking=True,
                             max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE,
                             txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_address(fresh_address))
        args.append(TransactionArgument.to_U8Vector(auth_key_prefix))

        ty_args = self.get_type_args(currency_module_address, currency_code)
        script = Script.gen_script(CodeType.CREATE_EMPTY_ACCOUNT, *args, ty_args=ty_args, currency_module_address=currency_module_address)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def empty_script(self, sender_account, is_blocking=True,
                     gas_currency_code=None, max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE, txn_expiration=TXN_EXPIRATION):
        args = []

        script = Script.gen_script(CodeType.EMPTY_SCRIPT, *args)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def grant_association_address(self, sender_account, address, is_blocking=True,
                                  max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE,
                                  txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_address(address))

        script = Script.gen_script(CodeType.GRANT_ASSOCIATION_ADDRESS, *args)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def grant_association_privilege(self, sender_account, address, currency_module_address=None, currency_code=None,
                                    is_blocking=True,
                                    max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE,
                                    txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_address(address))
        ty_args = self.get_type_args(currency_module_address, currency_code)
        script = Script.gen_script(CodeType.GRANT_ASSOCIATION_PRIVILEGE, *args, ty_args=ty_args, currency_module_address=address)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def grant_child_account(self, sender_account, child_address, is_blocking=True,
                            max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE,
                            txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_address(child_address))

        script = Script.gen_script(CodeType.GRANT_CHILD_ACCOUNT, *args)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def grant_parent_account(self, sender_account, child_account, is_blocking=True,
                             max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE,
                             txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_address(child_account))

        script = Script.gen_script(CodeType.GRANT_PARENT_ACCOUNT, *args)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def grant_vasp_account(self, root_vasp_addr, is_blocking=True,
                           gas_currency_code=None, max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE, txn_expiration=TXN_EXPIRATION):
        self.require_faucet_account()
        args = []
        args.append(TransactionArgument.to_address(root_vasp_addr))

        script = Script.gen_script(CodeType.GRANT_VASP_ACCOUNT, *args)
        return self.submit_script(self.faucet_account, script, is_blocking, max_gas_amount, gas_unit_price,
                                  txn_expiration)

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

    def mint_lbr(self, sender_account, amount_lbr, is_blocking=True,
                 gas_currency_code=None, max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE, txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_U64(amount_lbr))

        script = Script.gen_script(CodeType.MINT_LBR, *args)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def modify_publishing_option(self, sender_account, option, is_blocking=True,
                                 max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE,
                                 txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_U8Vector(option))

        script = Script.gen_script(CodeType.MODIFY_PUBLISHING_OPTION, *args)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def transfer_coin(self, sender_account, receiver_address, micro_coins, auth_key_prefix=None, currency_module_address=None,
                      currency_code=None, is_blocking=True, data=None,
                      gas_currency_code=None, max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE, txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_address(receiver_address))
        args.append(TransactionArgument.to_U8Vector(auth_key_prefix))
        args.append(TransactionArgument.to_U64(micro_coins))
        args.append(TransactionArgument.to_U8Vector(data, hex=False))
        args.append(TransactionArgument.to_U8Vector(""))

        ty_args = self.get_type_args(currency_module_address, currency_code)
        script = Script.gen_script(CodeType.PEER_TO_PEER_WITH_METADATA, *args, ty_args=ty_args, currency_module_address=currency_module_address)
        return self.submit_script(sender_account, script, is_blocking,self.get_gas_currency_code(currency_code, gas_currency_code), max_gas_amount, gas_unit_price, txn_expiration)

    def preburn(self, sender_account, amount, currency_module_address=None, currency_code=None, is_blocking=True,
                gas_currency_code=None, max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE, txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_U64(amount))
        ty_args = self.get_type_args(currency_module_address, currency_code)
        script = Script.gen_script(CodeType.PREBURN, *args, ty_args=ty_args, currency_module_address=currency_module_address)
        return self.submit_script(sender_account, script, is_blocking,self.get_gas_currency_code(currency_code, gas_currency_code), max_gas_amount, gas_unit_price, txn_expiration)

    def publish_shared_ed25519_public_key(self, sender_account, public_key, is_blocking=True,
                                          max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE,
                                          txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_U8Vector(public_key))

        script = Script.gen_script(CodeType.PUBLISH_SHARED_ED25519_PUBLIC_KEY, *args)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def recertify_child_account(self, sender_account, child_address, is_blocking=True,
                                max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE,
                                txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_address(child_address))

        script = Script.gen_script(CodeType.RECERTIFY_CHILD_ACCOUNT, *args)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def register_approved_payment(self, sender_account, public_key, is_blocking=True,
                                  max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE,
                                  txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_U8Vector(public_key))

        script = Script.gen_script(CodeType.REGISTER_APPROVED_PAYMENT, *args)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def register_preburner(self, sender_account, currency_module_address=None, currency_code=None, is_blocking=True,
                           gas_currency_code=None, max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE, txn_expiration=TXN_EXPIRATION):
        args = []
        ty_args = self.get_type_args(currency_module_address, currency_code)
        script = Script.gen_script(CodeType.RECERTIFY_CHILD_ACCOUNT, *args, ty_args=ty_args,
                                   currency_module_address=currency_module_address)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def register_validator(self, sender_account, consensus_pubkey, validator_network_signing_pubkey,
                           validator_network_identity_pubkey,
                           validator_network_address, fullnodes_network_identity_pubkey, fullnodes_network_address,
                           is_blocking=True,
                           gas_currency_code=None, max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE, txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_U8Vector(consensus_pubkey))
        args.append(TransactionArgument.to_U8Vector(validator_network_signing_pubkey))
        args.append(TransactionArgument.to_U8Vector(validator_network_identity_pubkey))
        args.append(TransactionArgument.to_address(validator_network_address))
        args.append(TransactionArgument.to_U8Vector(fullnodes_network_identity_pubkey))
        args.append(TransactionArgument.to_address(fullnodes_network_address))

        script = Script.gen_script(CodeType.REGISTER_VALIDATOR, *args)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def remove_association_address(self, sender_account, address, is_blocking=True,
                                   max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE,
                                   txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_address(address))

        script = Script.gen_script(CodeType.REMOVE_ASSOCIATION_ADDRESS, *args)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def remove_association_privilege(self, sender_account, address, currency_module_address=None, currency_code=None,
                                     is_blocking=True,
                                     max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE,
                                     txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_address(address))

        script = Script.gen_script(CodeType.REMOVE_ASSOCIATION_PRIVILEGE, *args)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def remove_child_account(self, sender_account, child_address, is_blocking=True,
                             max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE,
                             txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_address(child_address))

        script = Script.gen_script(CodeType.REMOVE_CHILD_ACCOUNT, *args)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def remove_parent_account(self, sender_account, parent_address, is_blocking=True,
                              max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE,
                              txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_address(parent_address))

        script = Script.gen_script(CodeType.REMOVE_PARENT_ACCOUNT, *args)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def remove_validator(self, sender_account, new_validator, is_blocking=True,
                         gas_currency_code=None, max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE, txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_address(new_validator))

        script = Script.gen_script(CodeType.REMOVE_VALIDATOR, *args)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def rotate_authentication_key(self, sender_account, new_key, is_blocking=True,
                                  max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE,
                                  txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_address(new_key))

        script = Script.gen_script(CodeType.ROTATE_AUTHENTICATION_KEY, *args)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def rotate_consensus_pubkey(self, sender_account, new_key, is_blocking=True,
                                max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE,
                                txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_address(new_key))

        script = Script.gen_script(CodeType.ROTATE_CONSENSUS_PUBKEY, *args)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def rotate_shared_ed25519_public_key(self, sender_account, public_key, is_blocking=True,
                                         max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE,
                                         txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_address(public_key))

        script = Script.gen_script(CodeType.ROTATE_SHARED_ED25519_PUBLIC_KEY, *args)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def unmint_lbr(self, sender_account, amount_lbr, is_blocking=True,
                   gas_currency_code=None, max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE, txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_U64(amount_lbr))

        script = Script.gen_script(CodeType.UNMINT_LBR, *args)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def update_exchange_rate(self, sender_account, new_exchange_rate_denominator, new_exchange_rate_numerator,
                             currency_module_address=None, currency_code=None, is_blocking=True,
                             max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE,
                             txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_U64(new_exchange_rate_denominator))
        args.append(TransactionArgument.to_U64(new_exchange_rate_numerator))

        ty_args = self.get_type_args(currency_module_address, currency_code)
        script = Script.gen_script(CodeType.UPDATE_EXCHANGE_RATE, *args, ty_args=ty_args, currency_module_address=currency_module_address)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def update_libra_version(self, sender_account, major, is_blocking=True,
                             max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE,
                             txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_U64(major))

        script = Script.gen_script(CodeType.UPDATE_LIBRA_VERSION, *args)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def update_minting_ability(self, sender_account, allow_minting, currency_module_address=None, currency_code=None,
                               is_blocking=True,
                               max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE,
                               txn_expiration=TXN_EXPIRATION):
        args = []
        args.append(TransactionArgument.to_bool(allow_minting))
        ty_args = self.get_type_args(currency_module_address, currency_code)
        script = Script.gen_script(CodeType.UPDATE_MINTING_ABILITY, *args, ty_args=ty_args,
                                   currency_module_address=currency_module_address)
        return self.submit_script(sender_account, script, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)

    def publish_token(self, sender_account: Account, currency_code=None, is_blocking=True, max_gas_amount=MAX_GAS_AMOUNT, gas_unit_price=GAS_UNIT_PRICE,
                       txn_expiration=TXN_EXPIRATION):
        module = Module.gen_module(sender_account.address, currency_code)
        return self.submit_module(sender_account, module, is_blocking, max_gas_amount, gas_unit_price, txn_expiration)


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



