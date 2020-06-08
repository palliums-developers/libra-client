from typing import Optional
from lbrtypes.account_state import AccountState as LibraAccountState
from lbrtypes.move_core.language_storage import TypeTag, StructTag
from banktypes.account_resources import TokensResource, UserInfoResource, TokenInfoStoreResource, LibraTokenResource
from error import get_exception

class AccountState(LibraAccountState):

    @classmethod
    def new(cls, account_state: LibraAccountState):
        ret = cls()
        ret.ordered_map = account_state.ordered_map
        return ret

    @get_exception
    def get_tokens_resource(self, bank_module_address=None) -> Optional[TokensResource]:
        resource = self.ordered_map.get(TokensResource.resource_path_for(module_address=self.get_bank_module_address(bank_module_address)))
        return TokensResource.deserialize(resource)

    @get_exception
    def get_user_info_resource(self, bank_module_address=None):
        resource = self.ordered_map.get(
            UserInfoResource.resource_path_for(module_address=self.get_bank_module_address(bank_module_address)))
        return UserInfoResource.deserialize(resource)

    @get_exception
    def get_token_info_store_resource(self) -> Optional[TokenInfoStoreResource]:
        self.require_bank_account()
        resource = self.ordered_map.get(
            TokenInfoStoreResource.resource_path_for(module_address=self.get_account_address()))
        return TokenInfoStoreResource.deserialize(resource)

    @get_exception
    def get_token_info(self, index):
        token_info_store = self.get_token_info_store_resource()
        return token_info_store.tokens[index]

    @get_exception
    def get_libra_token_resource(self, token_name, token_module_address=None):
        self.require_bank_account()
        type_tag = TypeTag("Struct", StructTag.new(token_module_address, token_name))
        resource = self.ordered_map.get(
            LibraTokenResource.resource_path_for(type_tag, module_address=self.get_account_address())
        )
        return LibraTokenResource.deserialize(resource)

    @get_exception
    def get_bank_amount(self, index, bank_module_address=None):
        resource = self.get_tokens_resource(self.get_bank_module_address(bank_module_address))
        return resource.ts[index].value

    @get_exception
    def get_lock_amount(self, index, exchange_rate, bank_module_address=None):
        resource = self.get_tokens_resource(self.get_bank_module_address(bank_module_address))
        return self.mantissa_mul(resource.ts[index+1].value, exchange_rate)

    @get_exception
    def get_cur_lock_rate(self, token_name, token_module_address=None):
        exchange_rate = self.get_exchange_rate(token_name, token_module_address)
        exchange_rate_one_miniter_later = self.get_exchange_rate(token_name, token_module_address, lag_time=1)
        return (exchange_rate_one_miniter_later - exchange_rate) / exchange_rate

    @get_exception
    def get_borrow_amount(self, index, cur_interest_index=None, bank_module_address=None, include_interest=False):
        borrow_info = self.get_tokens_resource(self.get_bank_module_address(bank_module_address)).borrows[index]
        if not include_interest:
            return borrow_info.principal
        return self.mantissa_div(self.mantissa_mul(borrow_info.principal, cur_interest_index), borrow_info.interest_index)

    @get_exception
    def get_borrow_interest(self, index, cur_interest_index, bank_module_address=None):
        all_borrow = self.get_borrow_amount(index, cur_interest_index, bank_module_address, include_interest=True)
        origin_borrow = self.get_borrow_amount(index, cur_interest_index, bank_module_address, include_interest=False)
        return all_borrow - origin_borrow

    @get_exception
    def get_cur_borrow_rate(self, token_name, token_module_address=None):
        self.require_bank_account()
        max_borrowed = self.get_max_borrowed_balance(token_name, token_module_address)
        reserves = self.get_reserves(token_name, token_module_address)
        total_borrows = self.get_total_borrows_balance(token_name, token_module_address)
        return self.get_borrow_rate(total_borrows, max_borrowed, reserves) / 2**32

    @get_exception
    def get_utilization(self, token_name, token_module_address=None):
        total_borrow = self.get_total_borrows_balance(token_name, token_module_address)
        total_supply = self.get_total_supplied_balance(token_name, token_module_address)
        return total_borrow/total_supply

    @get_exception
    def get_token_index(self, token_name, token_module_address=None):
        self.require_bank_account()
        libra_token = self.get_libra_token_resource(token_name, token_module_address)
        return libra_token.index

    @get_exception
    def get_exchange_rate(self, token_name, token_module_address=None, lag_time=0):
        self.require_bank_account()
        index = self.get_token_index(token_name, token_module_address)
        total_borrows, total_reserves, _ = self.get_cur_interest_index(index, lag_time)
        token = self.get_tokens_resource(self.get_account_address()).ts[index]
        token_infos = self.get_token_info_store_resource()
        bank_token_info = token_infos.tokens[index+1]
        if bank_token_info.total_supply == 0:
            return self.new_mantissa(1, 100)
        return self.new_mantissa(token.value + total_borrows-total_reserves, bank_token_info.total_supply)

    @get_exception
    def get_cur_interest_index(self, index, lag_time = 0):
        self.require_bank_account()
        self.require_bank_account()
        t = self.get_tokens_resource(self.get_account_address()).ts[index]
        ti = self.get_token_info_store_resource().tokens[index]
        borrow_rate = self.get_borrow_rate(ti.total_borrows, t.value, ti.total_reserves)
        ti = self.get_token_info_store_resource().tokens[index]
        import time
        minute = int(time.time() / 60) - ti.last_minute + lag_time
        borrow_rate = borrow_rate* minute
        interest_accumulated = self.mantissa_mul(ti.total_borrows, borrow_rate)
        total_borrows = ti.total_borrows + interest_accumulated
        resesrve_factor = self.new_mantissa(1, 20)
        total_reserves = ti.total_reserves + self.mantissa_mul(interest_accumulated, resesrve_factor)
        borrow_index = ti.borrow_index + self.mantissa_mul(ti.borrow_index, borrow_rate)
        return total_borrows, total_reserves, borrow_index

    @get_exception
    def get_borrow_info(self, index, bank_module_address=None):
        resource = self.get_tokens_resource(self.get_bank_module_address(bank_module_address))
        return resource.borrows[index]

    @get_exception
    def get_total_supplied_balance(self, token_name, token_module_address=None):
        self.require_bank_account()
        index = self.get_token_index(token_name, token_module_address)
        total_supply = self.get_token_info(index+1).total_supply
        return self._lock_to_base_assert(token_name, total_supply)

    @get_exception
    def get_reserves(self, token_name, token_module_address=None):
        self.require_bank_account()
        index = self.get_token_index(token_name, token_module_address)
        _, total_reserves, _ = self.get_cur_interest_index(index)
        return self._lock_to_base_assert(token_name, total_reserves)

    @get_exception
    def get_total_borrows_balance(self, token_name, token_module_address=None):
        self.require_bank_account()
        index = self.get_token_index(token_name, token_module_address)
        total_borrow = self.get_token_info(index).total_borrows
        borrow_index = self.get_token_info(index).borrow_index
        return self._borrow_to_base_assert(token_name, total_borrow, borrow_index)

    @get_exception
    def get_borrow_rate(self, total_borrows, max_borrowed, total_reserves):
        if max_borrowed <= total_reserves:
            util = self.new_mantissa(1, 1)
        else:
            util = self.new_mantissa(total_borrows, max_borrowed+total_borrows-total_reserves)
        baserate_perminute = self.new_mantissa(5*60*24*30, 100*60*24*365)
        return baserate_perminute + self.mantissa_mul(baserate_perminute, util)

    def get_max_borrowed_balance(self, token_name, token_module_address=None):
        return self.get_total_supplied_balance(token_name, token_module_address) - self.get_total_borrows_balance(token_name, token_module_address)

    def get_collateral_factor(self):
        pass

    def set_bank_module_address(self, address):
        if address:
            self.bank_module_address = address

    def get_bank_module_address(self, address=None):
        if address:
            return address
        if hasattr(self, "bank_module_address"):
            return self.bank_module_address

    def require_bank_account(self):
        resource = self.ordered_map.get(
            TokenInfoStoreResource.resource_path_for(module_address=self.get_account_address()))
        assert(resource is not None)

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

    def _borrow_to_base_assert(self, token_name, amount, corresponding_interest_index, token_module_address=None):
        self.require_bank_account()
        index = self.get_token_index(token_name, token_module_address)
        _, _, cur_interest_index = self.get_cur_interest_index(index)
        return self.mantissa_div(self.mantissa_mul(amount, cur_interest_index), corresponding_interest_index)

    def _lock_to_base_assert(self, token_name, amount, token_module_address=None):
        self.require_bank_account()
        exchange_rate = self.get_exchange_rate(token_name, token_module_address)
        return self.mantissa_mul(amount, exchange_rate)




