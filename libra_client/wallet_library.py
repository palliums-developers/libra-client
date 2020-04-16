from mnemonic import Mnemonic
from typing import Dict
from libra_client.key_factory import KeyFactory
from libra.rustlib import ensure
from libra.account import Account
from libra.account_address import Address
from libra.transaction.raw_transaction import RawTransaction
from libra.transaction.signed_transaction import SignedTransaction
import os

class Wallet():
    DELIMITER = ";"
    def __init__(self, mnemonic: bytes, key_factory: KeyFactory, addr_map: Dict[Address, int], key_leaf: Dict):
        self.mnemonic = mnemonic
        self.key_factory = key_factory
        self.addr_map = addr_map
        self.key_leaf = key_leaf

    @classmethod
    def new(cls):
        m = Mnemonic("english")
        mnemonic = m.generate(192)
        return cls.new_from_mnemonic(mnemonic)

    @classmethod
    def new_from_mnemonic(cls, mnemonic):
        seed = KeyFactory.to_seed(mnemonic)
        key_factory = KeyFactory(seed)
        return cls(mnemonic, key_factory, {}, 0)

    def write_recovery(self, out_file_path: str):
        with open(out_file_path, 'wt') as f:
            f.write(self.mnemonic)
            f.write(self.DELIMITER)
            f.write(str(self.key_leaf))

    @staticmethod
    def recover(input_file_path: str):
        if os.path.exists(input_file_path):
            with open(input_file_path) as f:
                data = f.read()
                arr = data.split(Wallet.DELIMITER)
                ensure(len(arr) == 2, "Format Error: Wallet must has child num")
                wallet = Wallet.new_from_mnemonic(arr[0])
                wallet.generate_addresses(arr[1])
                return wallet

    def generate_addresses(self, depth: int):
        ensure(self.key_leaf <= depth, f"Addresses already generated up to the supplied depth")
        while self.key_leaf != depth:
            self.new_address()

    def new_address_at_child_number(self, child_number):
        child = self.key_factory.private_child(child_number)
        return Account(child).address

    def new_account(self):
        child = Account(self.key_factory.private_child(self.key_leaf))
        old_key_leaf = self.key_leaf
        self.key_leaf += 1
        ensure(self.addr_map.get(child.address) is None, f"This address is already in your wallet" )
        self.addr_map[child.address] = old_key_leaf
        return child
        # return authentication_key, old_key_leaf

    def get_addresses(self):
        rev_map = { index: addr for addr, index in self.addr_map.items()}
        ret = list()
        for i in range(len(self.addr_map)):
            address = rev_map.get(i)
            ensure(address is not None, f"Child num {i} not exist while depth is {len(self.addr_map)}")
            ret.append(address)
        return ret

    def sign_txn(self, tx: RawTransaction):
        child = self.addr_map.get(tx.sender)
        ensure(child is not None, "Well, that address is nowhere to be found... This is awkward")
        child_key = self.key_factory.private_child(child)
        return SignedTransaction.gen_from_raw_txn(tx, Account(child_key))