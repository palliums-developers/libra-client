from violas_client.json_rpc.views import TransactionView as LibraTransactionView
from violas_client.extypes.bytecode import get_code_type, CodeType
from violas_client.lbrtypes.bytecode import CodeType as LibraCodeType
from violas_client.extypes.exchange_resource import *

class TransactionView(LibraTransactionView):

    type_maps = {
        CodeType.ADD_LIQUIDITY: MintEvent,
        CodeType.REMOVE_LIQUIDITY: BurnEvent,
        CodeType.SWAP: SwapEvent,
        CodeType.WITHDRAW_MINE_REWARD: RewardEvent,
    }

    @classmethod
    def new(cls, tx):
        ret = tx
        ret.__class__ = TransactionView
        return ret

    def get_code_type(self):
        type = super().get_code_type()
        if type == LibraCodeType.UNKNOWN:
            return get_code_type(self.get_script_hash())
        return type

    def get_swap_events(self):
        code_type = self.get_code_type()
        if code_type in CodeType:
            events = []
            if code_type in CodeType:
                for event in self.get_events():
                    if event.data.enum_name == "Unknown":
                        try:
                            events.append(Event.deserialize(bytes.fromhex(event.data.value.raw)))
                        except:
                            pass
        return events

    def get_swap_type_events(self, t):
        ret = []
        event_type = self.type_maps.get(t)
        for event in self.get_swap_events():
            if isinstance(event.get_swap_event(), event_type):
                ret.append(event)
        return ret

    def get_swap_timestamp(self):
        events = self.get_swap_events()
        if len(events):
            return events[0].timestamp

    def get_swap_reward_amount(self):
        events = self.get_swap_events()
        for event in events:
            e = event.get_swap_event()
            if isinstance(e, RewardEvent):
                return e.reward_amount

    def get_receiver(self):
        receiver = super().get_receiver()
        if receiver is None and self.get_code_type() in (CodeType.SWAP, ):
            if len(self.events) > 0:
                return self.events[-1].get_address()
        return receiver


    def __str__(self):
        import json
        amap = self.to_json_serializable()
        swap_event = self.get_swap_event()
        if swap_event:
            amap["swap_event"] = swap_event.to_json_serializable()
        return json.dumps(amap, sort_keys=False, indent=2)





