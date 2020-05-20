from canoser import Struct
from lbrtypes.move_core.language_storage import TypeTag
from lbrtypes.transaction.transaction_argument import TransactionArgument
from lbrtypes.bytecode import get_code_type, get_code

SCRIPT_HASH_LENGTH = 32

class Script(Struct):
    _fields = [
        ("code", bytes),
        ("ty_args", [TypeTag]),
        ("args", [TransactionArgument]),
    ]

    def get_code_type(self):
        return get_code_type(self.code)

    def get_code(self):
        return self.code.hex()

    def get_ty_args(self):
        return self.ty_args

    def get_args(self):
        return self.args

    @staticmethod
    def gen_script(code_type, *args, ty_args=None, module_address=None):
        code = get_code(code_type, module_address)
        if ty_args is None:
            ty_args = []
        return Script(code, ty_args, list(args))

    # @staticmethod
    # def parse_data(data):
    #     if data is None:
    #         data = b""
    #     if isinstance(data, str):
    #         data = str.encode(data, encoding="utf-8")
    #     return data
    #
    # @classmethod
    # def gen_add_currency_script(cls, exchange_rate_denom, exchange_rate_num, is_synthetic, scaling_factor, fractional_part, currency_code, module_address, module_name):
    #     module_address = AccountAddress.normalize_to_bytes(module_address)
    #     if isinstance(currency_code, str):
    #         currency_code = str.encode(currency_code)
    #     code = get_code(CodeType.ADD_CURRENCY)
    #     args = [
    #         TransactionArgument('U64', exchange_rate_denom),
    #         TransactionArgument('U64', exchange_rate_num),
    #         TransactionArgument('Bool', is_synthetic),
    #         TransactionArgument('U64', scaling_factor),
    #         TransactionArgument('U64', fractional_part),
    #         TransactionArgument('U8Vector', currency_code),
    #     ]
    #
    #     ty_args = [get_coin_type(module_address, module_name)]
    #     return Script(code, ty_args, args)
    #
    # @classmethod
    # def gen_apply_for_child_vasp_credential_script(cls, root_vasp_address):
    #     root_vasp_address = AccountAddress.normalize_to_bytes(root_vasp_address)
    #     code = get_code(CodeType.APPLY_FOR_CHILD_VASP_CREDENTIAL)
    #     args = [
    #         TransactionArgument('Address', root_vasp_address),
    #     ]
    #     return Script(code, [], args)
    #
    # @classmethod
    # def gen_allow_child_accounts(cls):
    #     code = get_code(CodeType.ALLOW_CHILD_ACCOUNTS)
    #     args = [
    #     ]
    #     return Script(code, [], args)
    #
    # @classmethod
    # def gen_transfer_script(cls,
    #     receiver_address,
    #     micro_libra,
    #     metadata=None,
    #     auth_key_prefix=None,
    #     module_address=None,
    #     module_name=None
    # ):
    #     receiver_address = AccountAddress.normalize_to_bytes(receiver_address)
    #     if auth_key_prefix is None:
    #         auth_key_prefix = b""
    #     else:
    #         auth_key_prefix = AccountAddress.normalize_to_bytes(auth_key_prefix)
    #     metadata = cls.parse_data(metadata)
    #     metadata_signature = b''
    #     code = get_code(CodeType.VCOIN_TRANSFER_WITH_DATA)
    #     args = [
    #         TransactionArgument('Address', receiver_address),
    #         TransactionArgument('U8Vector', auth_key_prefix),
    #         TransactionArgument('U64', micro_libra),
    #         TransactionArgument('U8Vector', metadata),
    #         TransactionArgument('U8Vector', metadata_signature)
    #     ]
    #     ty_args = [get_coin_type(module_address, module_name)]
    #     return Script(code, ty_args, args)
    #
    # @classmethod
    # def gen_mint_script(cls, receiver_address, auth_key_prefix, micro_libra, module_address, module_name):
    #     receiver_address = AccountAddress.normalize_to_bytes(receiver_address)
    #     if auth_key_prefix is None:
    #         auth_key_prefix = b""
    #     code = bytecodes["mint"]
    #     args = [
    #             TransactionArgument('Address', receiver_address),
    #             TransactionArgument('U8Vector', auth_key_prefix),
    #             TransactionArgument('U64', micro_libra)
    #         ]
    #     ty_args = [get_coin_type(module_address, module_name)]
    #     return Script(code, ty_args, args)
    #
    # @classmethod
    # def gen_create_account_script(cls, fresh_address, auth_key_prefix, initial_balance=0):
    #     fresh_address = AccountAddress.normalize_to_bytes(fresh_address)
    #     code = bytecodes["create_account"]
    #     args = [
    #             TransactionArgument('Address', fresh_address),
    #             TransactionArgument('U8Vector', auth_key_prefix),
    #             TransactionArgument('U64', initial_balance)
    #         ]
    #     ty_args = [lbr_type_tag()]
    #     return Script(code, ty_args, args)
    #
    # @classmethod
    # def gen_rotate_auth_key_script(cls, public_key):
    #     key = normalize_public_key(public_key)
    #     code = bytecodes["rotate_authentication_key"]
    #     args = [
    #             TransactionArgument('U8Vector', key)
    #         ]
    #     return Script(code, [], args)
    #
    # @classmethod
    # def gen_rotate_consensus_pubkey_script(cls, public_key):
    #     key = normalize_public_key(public_key)
    #     code = bytecodes["rotate_consensus_pubkey"]
    #     args = [
    #             TransactionArgument('U8Vector', key)
    #         ]
    #     return Script(code, [], args)
    #
    #
    # @classmethod
    # def gen_add_validator_script(cls, address):
    #     address = AccountAddress.normalize_to_bytes(address)
    #     code = bytecodes["add_validator"]
    #     args = [
    #             TransactionArgument('Address', address)
    #         ]
    #     return Script(code, [], args)
    #
    #
    # @classmethod
    # def gen_remove_validator_script(cls, address):
    #     address = AccountAddress.normalize_to_bytes(address)
    #     code = bytecodes["remove_validator"]
    #     args = [
    #             TransactionArgument('Address', address)
    #         ]
    #     return Script(code, [], args)
    #
    #
    # @classmethod
    # def gen_register_validator_script(cls,
    #     consensus_pubkey,
    #     validator_network_signing_pubkey,
    #     validator_network_identity_pubkey,
    #     validator_network_address,
    #     fullnodes_network_identity_pubkey,
    #     fullnodes_network_address
    #     ):
    #     validator_network_address = AccountAddress.normalize_to_bytes(validator_network_address)
    #     fullnodes_network_address = AccountAddress.normalize_to_bytes(fullnodes_network_address)
    #     consensus_pubkey = normalize_public_key(consensus_pubkey)
    #     validator_network_signing_pubkey = normalize_public_key(validator_network_signing_pubkey)
    #     validator_network_identity_pubkey = normalize_public_key(validator_network_identity_pubkey)
    #     fullnodes_network_identity_pubkey = normalize_public_key(fullnodes_network_identity_pubkey)
    #     code = bytecodes["register_validator"]
    #     args = [
    #             TransactionArgument('U8Vector', consensus_pubkey),
    #             TransactionArgument('U8Vector', validator_network_signing_pubkey),
    #             TransactionArgument('U8Vector', validator_network_identity_pubkey),
    #             TransactionArgument('Address', validator_network_address),
    #             TransactionArgument('U8Vector', fullnodes_network_identity_pubkey),
    #             TransactionArgument('Address', fullnodes_network_address)
    #         ]
    #     return Script(code, [], args)


