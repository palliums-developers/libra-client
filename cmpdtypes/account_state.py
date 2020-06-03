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

    def get_bank_amount(self, index, bank_module_address=None):
        resource = self.get_tokens_resource(self.get_bank_module_address(bank_module_address))
        if resource and len(resource.ts) > index:
            return resource.ts[index].value

    def get_locked_amount(self, index, exchange_rate, bank_module_address=None):
        resource = self.get_tokens_resource(self.get_bank_module_address(bank_module_address))
        if resource and len(resource.ts) > index:
            return self.mantissa_mul(resource.ts[index+1].value, exchange_rate)

    def get_token_index(self, token_name, token_module_address=None):
        libra_token = self.get_libra_token_resource(token_name, token_module_address)
        if libra_token:
            return libra_token.index

    def get_exchange_rate(self, token_name, token_module_address=None):
        index = self.get_token_index(token_name, token_module_address)
        if index is not None:
            total_borrows, total_reserves, _ = self.get_cur_interest_index(index, token_module_address)
            token = self.get_tokens_resource(self.get_account_address()).ts[index]
            token_infos = self.get_token_info_store_resource()
            bank_token_info = token_infos.tokens[index+1]
            if bank_token_info.total_supply == 0:
                return self.new_mantissa(1, 100)
            print("total_borrow = ", total_borrows)
            print("totoal_reserves =", total_reserves)
            print(token.value + total_borrows-total_reserves , bank_token_info.total_supply)
            return self.new_mantissa(token.value + total_borrows-total_reserves , bank_token_info.total_supply)

    def get_borrow_rate(self, index, bank_module_address=None):
        try:
            bank_module_address = self.get_bank_module_address(bank_module_address)
            t = self.get_tokens_resource(bank_module_address).ts[index]
            ti = self.get_token_info_store_resource().tokens[index]
            if t.value <= ti.total_reserves:
                util = self.new_mantissa(1, 1)
            else:
                util = self.new_mantissa(ti.total_borrows, t.value+ti.total_borrows-ti.total_reserves)
            baserate_perminute = self.new_mantissa(5, 100*60*24*365)
            return baserate_perminute + self.mantissa_mul(baserate_perminute, util)
        except:
            pass

    def get_cur_interest_index(self, index, bank_module_address=None):
        bank_module_address = self.get_bank_module_address(bank_module_address)
        borrow_rate = self.get_borrow_rate(index)
        ti = self.get_token_info_store_resource(bank_module_address).tokens[index]
        import time
        minute = int(time.time() / 60) - ti.last_minute
        borrow_rate = borrow_rate* minute
        interest_accumulated = self.mantissa_mul(ti.total_borrows, borrow_rate)
        total_borrows = ti.total_borrows + interest_accumulated
        resesrve_factor = self.new_mantissa(1, 20)
        total_reserves = ti.total_reserves + self.mantissa_mul(interest_accumulated, resesrve_factor)
        borrow_index = ti.borrow_index + self.mantissa_mul(ti.borrow_index, borrow_rate)
        return total_borrows, total_reserves, borrow_index


    def get_borrow_info(self, index, bank_module_address=None):
        resource = self.get_tokens_resource(self.get_bank_module_address(bank_module_address))
        if resource and len(resource.borrows) > index:
            return resource.borrows[index]

    def get_borrowed_amount(self, index, cur_interest_index, bank_module_address=None):
        try:
            borrow_info = self.get_tokens_resource(self.get_bank_module_address(bank_module_address)).borrows[index]
            return self.mantissa_div(self.mantissa_mul(borrow_info.principal, cur_interest_index), borrow_info.interest_index)
        except:
            pass

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



