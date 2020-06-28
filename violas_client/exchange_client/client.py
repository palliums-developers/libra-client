from typing import Optional, Union
from libra_client import Client as LibraClient
from extypes.transaction.module import Module
from extypes.transaction.script import Script
from lbrtypes.transaction.transaction_argument import TransactionArgument
from extypes.bytecode import CodeType
from extypes.account_state import AccountState
from extypes.view import TransactionView
from extypes.bytecode import update_hash_to_type_map
from lbrtypes.rustlib import ensure
from extypes.exchange_resource import ReservesResource
from dijkstra import Graph, DijkstraSPF
from extypes.exchange_error import ExchangeError
from error import LibraError

class Client(LibraClient):

    DEAD_LINE = 7258089600

    def swap_publish_contract(self, sender_account, is_blocking=True, **kwargs):
        module = Module.gen_module(CodeType.EXDEP,sender_account.address)
        self.submit_module(sender_account, module, is_blocking, **kwargs)
        module = Module.gen_module(CodeType.EXCHANGE,sender_account.address)
        return self.submit_module(sender_account, module, is_blocking, **kwargs)

    def swap_add_currency(self, exchange_account, currency_code, is_blocking=True, **kwargs):
        exchange_module_address = self.get_exchange_module_address()
        args = []
        ty_args = self.get_type_args(currency_code)
        script = Script.gen_script(CodeType.ADD_CURRENCY, *args, ty_args=ty_args, module_address=exchange_module_address)
        seq = self.submit_script(exchange_account, script, is_blocking, **kwargs)
        self.swap_update_registered_currencies()
        return seq

    def swap_add_liquidity(self, sender_account, currencya_code, currencyb_code, amounta_desired, amountb_desired, amounta_min=None, amountb_min=None, is_blocking=True, **kwargs):
        exchange_module_address = self.get_exchange_module_address()
        if amounta_min is None:
            amounta_min = 0
        if amountb_min is None:
            amountb_min = 0
        indexa = self.swap_get_currency_index(currencya_code)
        indexb = self.swap_get_currency_index(currencyb_code)
        if indexa > indexb:
            currencya_code, currencyb_code = currencyb_code, currencya_code
            amounta_desired, amountb_desired = amountb_desired, amounta_desired
            amounta_min, amountb_min = amountb_min, amounta_min

        ty_args = self.get_type_args(currencya_code)
        ty_args.extend(self.get_type_args(currencyb_code))

        args = []
        args.append(TransactionArgument.to_U64(amounta_desired))
        args.append(TransactionArgument.to_U64(amountb_desired))
        args.append(TransactionArgument.to_U64(amounta_min))
        args.append(TransactionArgument.to_U64(amountb_min))

        script = Script.gen_script(CodeType.ADD_LIQUIDITY, *args, ty_args=ty_args, module_address=exchange_module_address)
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def swap_initialize(self, module_account, is_blocking=True, **kwargs):
        exchange_module_address = module_account.address
        args = []
        ty_args = []

        script = Script.gen_script(CodeType.INITIALIZE, *args, ty_args=ty_args, module_address=exchange_module_address)
        return self.submit_script(module_account, script, is_blocking, **kwargs)

    def swap_remove_liquidity(self, sender_account, currencya_code, currencyb_code, liquidity, amounta_min=0, amountb_min=0, is_blocking=True, **kwargs):
        exchange_module_address = self.get_exchange_module_address()
        indexa = self.swap_get_currency_index(currencya_code)
        indexb = self.swap_get_currency_index(currencyb_code)
        if indexa > indexb:
            currencya_code, currencyb_code = currencyb_code, currencya_code
            amounta_min, amountb_min = amountb_min, amounta_min
        args = []
        args.append(TransactionArgument.to_U64(liquidity))
        args.append(TransactionArgument.to_U64(amounta_min))
        args.append(TransactionArgument.to_U64(amountb_min))

        ty_args = self.get_type_args(currencya_code)
        ty_args.extend(self.get_type_args(currencyb_code))

        script = Script.gen_script(CodeType.REMOVE_LIQUIDITY, *args, ty_args=ty_args, module_address=exchange_module_address)
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def swap(self, sender_account, currency_in_code, currency_out_code, amount_in, amount_out_min=0, is_blocking=True, **kwargs):
        exchange_module_address = self.get_exchange_module_address()
        indexa = self.swap_get_currency_index(currency_in_code)
        indexb = self.swap_get_currency_index(currency_out_code)
        if indexa > indexb:
            currency_in_code, currency_out_code = currency_out_code, currency_in_code
        ensure(indexa is not None, f"Can not find index of {currency_in_code} ")
        ensure(indexb is not None, f"Can not find index of {currency_out_code} ")
        path = self.swap_get_path(indexa, indexb)
        args = []
        args.append(TransactionArgument.to_U64(amount_in))
        args.append(TransactionArgument.to_U64(amount_out_min))
        args.append(TransactionArgument.to_U8Vector(bytes(path)))

        ty_args = self.get_type_args(currency_in_code)
        ty_args.extend(self.get_type_args(currency_out_code))

        script = Script.gen_script(CodeType.SWAP, *args, ty_args=ty_args, module_address= exchange_module_address)
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def get_transaction(self, version, fetch_events:bool=True) -> Optional[TransactionView]:
        txs = self.get_transactions(version, 1, fetch_events)
        if len(txs):
            return txs[0]

    def get_transactions(self, start_version: int, limit: int, fetch_events: bool=True) -> [TransactionView]:
        txs = super().get_transactions(start_version, limit, fetch_events)
        return [TransactionView.new(tx) for tx in txs]

    def get_account_transaction(self, account_address: Union[bytes, str], sequence_number: int, fetch_events: bool=True) -> TransactionView:
        tx = super().get_account_transaction(account_address, sequence_number, fetch_events)
        if tx:
            return TransactionView.new(tx)

    def get_exchange_module_address(self, exchange_module_address=None):
        if exchange_module_address:
            return exchange_module_address
        if hasattr(self, "exchange_module_address"):
            return self.exchange_module_address
        ensure(False, "Not set exchange module address")

    def set_exchange_module_address(self, exchange_module_address):
        self.exchange_module_address = exchange_module_address
        update_hash_to_type_map(exchange_module_address)
        self.swap_update_registered_currencies()

    def swap_get_account_blob(self, account_address) -> Optional[AccountState]:
        blob = super().get_account_blob(account_address)
        if blob:
            state = AccountState.new(blob)
            state.set_exchange_module_address(self.get_exchange_module_address())
            return state

    def swap_get_account_state(self, account_address) -> Optional[AccountState]:
        blob = super().get_account_blob(account_address)
        if blob:
            state = AccountState.new(blob)
            state.set_exchange_module_address(self.get_exchange_module_address())
            return state

    def swap_get_reserves_resource(self) -> Optional[ReservesResource]:
        exchange_module_address = self.get_exchange_module_address()
        blob = super().get_account_blob(exchange_module_address)
        if blob:
            state = AccountState.new(blob)
            return state.swap_get_reserves_resource()
        return []

    def swap_get_liquidity_balances(self, liquidity_address):
        exchange_module_address = self.get_exchange_module_address()
        state = self.swap_get_account_state(liquidity_address)
        if state:
            currencies = []
            reserves = self.swap_get_reserves_resource()
            resource = state.swap_get_tokens_resource(exchange_module_address)
            for token in resource.tokens:
                index = token.index
                value = token.value
                indexa = index >> 32
                indexb = index & 0xffffffff
                amounts = self.liquidity_to_currencies(reserves, indexa, indexb, value)
                if amounts is not None:
                    codes = self.swap_get_currency_codes(indexa, indexb)
                    result = {
                        codes[0]: amounts[0],
                        codes[1]: amounts[1],
                        "liquidity": amounts[2]
                    }
                    currencies.append(result)
            return currencies

    def swap_get_expected_swap_amount(self, currency_in, currency_out, currency_in_amount):
        index_in = self.swap_get_currency_index(currency_in)
        index_out = self.swap_get_currency_index(currency_out)
        reserves = self.swap_get_reserves_resource()
        return self.currency_to_currency(reserves, index_in, index_out, currency_in_amount)

    def swap_get_expected_liquidity_amount(self, currency_in, currency_out, currency_in_amount):
        index_in = self.swap_get_currency_index(currency_in)
        index_out = self.swap_get_currency_index(currency_out)
        reserves = self.swap_get_reserves_resource()
        return self.liquidity_currency_to_currency(reserves, index_in, index_out, currency_in_amount)

    def swap_get_liquidity_pairs(self):
        if hasattr(self, "liquidity_pairs"):
            return self.liquidity_pairs
        return self.swap_update_liquidity_pairs()

    def swap_update_liquidity_pairs(self):
        exchange_module_address = self.get_exchange_module_address()
        state = self.swap_get_account_state(exchange_module_address)
        if state:
            reserves_resource = state.swap_get_reserves_resource()
            if reserves_resource:
                self.liquidity_pairs = Graph()
                for reserve in reserves_resource:
                    self.liquidity_pairs.add_edge(reserve.coina.index, reserve.coinb.index, 1)
                    self.liquidity_pairs.add_edge(reserve.coinb.index, reserve.coina.index, 1)
                return self.liquidity_pairs

    def swap_get_path(self, indexa, indexb):
        liquidity_pairs = self.swap_get_liquidity_pairs()

        dijkstra = DijkstraSPF(liquidity_pairs, indexa)
        try:
            return dijkstra.get_path(indexb)
        except KeyError:
            pass
        self.swap_update_liquidity_pairs()
        try:
            dijkstra = DijkstraSPF(liquidity_pairs, indexa)
            return dijkstra.get_path(indexb)
        except KeyError:
            raise LibraError(data = ExchangeError.PATH_ERROR, message=f"Can not find path from {indexa} to {indexb}")

    def swap_get_registered_currencies(self):
        if hasattr(self, "currency_codes"):
            return self.currency_codes
        return self.swap_update_registered_currencies()

    def swap_update_registered_currencies(self):
        exchange_module_address = self.get_exchange_module_address()
        state = self.swap_get_account_state(exchange_module_address)
        if state:
            registered_currencies = state.swap_get_registered_currencies(exchange_module_address)
            if registered_currencies:
                self.currency_codes = registered_currencies.currency_codes
                return self.currency_codes

    def swap_get_currency_index(self, currency_code):
        registered_currencies = self.swap_get_registered_currencies()
        ensure(registered_currencies is not None, "Registered_currencies is None")
        for index, code in enumerate(registered_currencies):
            if code == currency_code:
                return index
        self.swap_update_registered_currencies()
        for index, code in enumerate(registered_currencies):
            if code == currency_code:
                return index

    def swap_get_currency_indexs(self, *args):
        ret = []
        for coin_name in args:
            ret.append(self.swap_get_currency_index(coin_name))
        return ret

    def swap_get_currency_code(self, id):
        registered_currencies = self.swap_get_registered_currencies()
        ensure(registered_currencies is not None, "Registered currencies is None")
        if len(registered_currencies) <= id:
            self.swap_update_registered_currencies()
        ensure(len(registered_currencies) > id, f"Registered currencies has no id {id}")
        return registered_currencies[id]

    def swap_get_currency_codes(self, *args):
        ret = []
        for id in args:
            ret.append(self.swap_get_currency_code(id))
        return ret

    def get_reserve(self, reserves, indexa, indexb):
        min_index = min(indexa, indexb)
        max_index = max(indexa, indexb)
        for reserve in reserves:
            if min_index == reserve.coina.index and max_index == reserve.coinb.index:
                return reserve
        raise LibraError(data=ExchangeError.PATH_ERROR, message=f"Can not find path from {indexa} to {indexb}")

    def liquidity_to_currencies(self, reserves, indexa, indexb, liquidity_amount):
        reserve = self.get_reserve(reserves, indexa, indexb)
        liquidity_total_supply = reserve.liquidity_total_supply
        total_min = reserve.coina.value
        total_max = reserve.coinb.value
        if indexa > indexb:
            total_a = total_max
            total_b = total_min
        else:
            total_b = total_max
            total_a = total_min
        amounta = int(liquidity_amount * total_a / liquidity_total_supply)
        amountb = int(liquidity_amount * total_b / liquidity_total_supply)
        return amounta, amountb, liquidity_amount

    def currency_to_currency(self, reserves, index_in, index_out, currency_in_amount):
        path = self.swap_get_path(index_in, index_out)
        pre_node = None
        for node in path:
            if pre_node is None:
                pre_node = node
                continue
            reserve = self.get_reserve(reserves, pre_node, node)
            total_min = reserve.coina.value
            total_max = reserve.coinb.value
            if index_in > index_out:
                total_in = total_max
                total_out = total_min
            else:
                total_out = total_max
                total_in = total_min
            currency_in_amount = self.get_amount_out(currency_in_amount, total_in, total_out)
            pre_node = node
        return currency_in_amount


    @staticmethod
    def get_amount_out(amount_in, reserve_in, reserve_out):
        amount_in_with_fee = amount_in * 997
        numerator = amount_in_with_fee * reserve_out
        denominator = reserve_in * 1000 + amount_in_with_fee
        return int(numerator / denominator)


    def liquidity_currency_to_currency(self, reserves, index_in, index_out, currency_in_amount):
        path = self.swap_get_path(index_in, index_out)
        pre_node = None
        for node in path:
            if pre_node is None:
                pre_node = node
                continue
            reserve = self.get_reserve(reserves, pre_node, node)
            total_min = reserve.coina.value
            total_max = reserve.coinb.value
            if index_in > index_out:
                total_in = total_max
                total_out = total_min
            else:
                total_out = total_max
                total_in = total_min

            currency_in_amount = int(currency_in_amount * total_out / total_in)
        return currency_in_amount

