from typing import Optional
from lbrtypes.account_state import AccountState as LibraAccountState
from lbrtypes.move_core.language_storage import TypeTag, StructTag
from cmpdtypes.account_resources import TokensResource, UserInfoResource, TokenInfoStoreResource, LibraTokenResource

class AccountState(LibraAccountState):

    @classmethod
    def new(cls, account_state: LibraAccountState):
        ret = cls()
        ret.ordered_map = account_state.ordered_map
        return ret

    def get_tokens_resource(self, bank_module_address=None) -> Optional[TokensResource]:
        resource = self.ordered_map.get(TokensResource.resource_path_for(module_address=self.get_bank_module_address(bank_module_address)))
        if resource:
            return TokensResource.deserialize(resource)

    def get_user_info_resource(self, bank_module_address=None):
        resource = self.ordered_map.get(
            UserInfoResource.resource_path_for(module_address=self.get_bank_module_address(bank_module_address)))
        if resource:
            return UserInfoResource.deserialize(resource)

    def get_token_info_store_resource(self,bank_module_address=None) -> Optional[TokenInfoStoreResource]:
        resource = self.ordered_map.get(
            TokenInfoStoreResource.resource_path_for(module_address=self.get_bank_module_address(bank_module_address)))
        if resource:
            return TokenInfoStoreResource.deserialize(resource)

    def get_libra_token_resource(self, token_name, token_module_address=None):
        type_tag = TypeTag("Struct", StructTag.new(token_module_address, token_name))
        resource = self.ordered_map.get(
            LibraTokenResource.resource_path_for(type_tag, module_address=self.get_account_address())
        )
        if resource:
            return LibraTokenResource.deserialize(resource)

    def get_token_index(self, token_name, token_module_address=None):
        libra_token = self.get_libra_token_resource(token_name, token_module_address)
        if libra_token:
            return libra_token.index
    
    def get_borrow_index(self, token_name, token_module_address=None):
        index = self.get_token_index(token_name, token_module_address)
        if index is not None:
            token_info_store = self.get_token_info_store_resource(self.get_account_address())
            if token_info_store:
                return token_info_store.tokens[index].borrow_index

    def get_exchange_rate(self, token_name, token_module_address=None):
        index = self.get_token_index(token_name, token_module_address)
        if index is not None:
            token = self.get_tokens_resource(self.get_account_address()).ts[index]
            token_infos = self.get_token_info_store_resource()
            token_info = token_infos.tokens[index]
            bank_token_info = token_infos.tokens[index+1]
            if bank_token_info.total_supply == 0:
                return self.new_mantissa(100, 1)
            print(bank_token_info.total_supply, token.value, token_info.total_borrows, token_info.total_reserves)
            return self.new_mantissa(bank_token_info.total_supply, token.value+token_info.total_borrows-token_info.total_reserves)

    def get_bank_amount(self, index, bank_module_address=None):
        resource = self.get_tokens_resource(self.get_bank_module_address(bank_module_address))
        if resource and len(resource.ts) > index:
            return resource.ts[index].value

    def get_deposit_amount(self, index, bank_module_address=None):
        resource = self.get_tokens_resource(self.get_bank_module_address(bank_module_address))
        if resource and len(resource.ts) > index:
            return resource.ts[index+1].value

    def get_borrow_info(self, index, bank_module_address=None):
        resource = self.get_tokens_resource(self.get_bank_module_address(bank_module_address))
        if resource and len(resource.borrows) > index:
            return resource.borrows[index]

    def get_borrow_amount(self, index, borrow_index, bank_module_address=None):
        borrow_info = self.get_borrow_info(index, self.get_bank_module_address(bank_module_address))
        if borrow_info:
            return self.mantissa_div(self.mantissa_mul(borrow_info.principal, borrow_index), borrow_info.interest_index)


    # def get_borrow_balances(self, currency_codes):
    #     pass
    #
    # def get_deposit_balance(self, exchange_rate, token_name, token_module_address=None):
    #     pass
    #
    # def get_borrow_balance(self, exchange_rate, token_name, token_module_address=None):
    #     pass

    def set_bank_module_address(self, address):
        if address:
            self.bank_module_address = address

    def get_bank_module_address(self, address=None):
        if address:
            return address
        if hasattr(self, "bank_module_address"):
            return self.bank_module_address

    @staticmethod
    def new_mantissa(a, b):
        c = a << 64
        d = b << 32
        return int(c / d)

    @staticmethod
    def mantissa_div(a, b):
        c = a << 32
        d = c / b
        return int(d)

    @staticmethod
    def mantissa_mul(a, b):
        c = a * b
        return int(c >> 32)

    def __str__(self):
        import json
        str_amap = super().__str__()
        amap = json.loads(str_amap)
        tokens_resource = self.get_tokens_resource()
        user_info_resource = self.get_user_info_resource()
        token_info_store_resource = self.get_token_info_store_resource()
        if tokens_resource:
            amap["tokens_resource"] = tokens_resource.to_json_serializable()
        if user_info_resource:
            amap["user_info_resource"] = user_info_resource.to_json_serializable()
        if token_info_store_resource:
            amap["token_info_store_resource"] = token_info_store_resource.to_json_serializable()
        return json.dumps(amap, sort_keys=False, indent=2)



