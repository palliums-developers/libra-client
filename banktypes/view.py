from json_rpc.views import TransactionView as LibraTransactionView
from banktypes.bytecode import get_code_type, CodeType
from lbrtypes.bytecode import CodeType as LibraCodeType

WITH_AMOUNT_TYPE = [CodeType.BORROW, CodeType.ENTER_BANK, CodeType.EXIT_BANK, CodeType.LIQUIDATE_BORROW, CodeType.LOCK,
                    CodeType.REDEEM, CodeType.REPAY_BORROW]


class TransactionView(LibraTransactionView):
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

    def get_amount(self):
        amount = super().get_amount()
        if amount is None and self.get_code_type() in WITH_AMOUNT_TYPE:
            for event in self.get_events():
                if event.data.enum_name == "SentPayment":
                    return event.get_amount()
        return amount






