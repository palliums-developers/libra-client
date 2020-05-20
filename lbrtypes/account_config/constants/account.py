from lbrtypes.move_core.language_storage import ModuleId, StructTag, CORE_CODE_ADDRESS

ACCOUNT_MODULE_NAME = "LibraAccount"

# Account
ACCOUNT_MODULE_IDENTIFIER = "LibraAccount"
ACCOUNT_STRUCT_NAME =  "T"
ACCOUNT_BALANCE_STRUCT_NAME = "Balance"

#/ The ModuleId for the Account module.
ACCOUNT_MODULE = ModuleId(CORE_CODE_ADDRESS, ACCOUNT_MODULE_IDENTIFIER)

# Payment Events
SENT_EVENT_NAME = "SentPaymentEvent"

RECEIVED_EVENT_NAME = "ReceivedPaymentEvent"

def account_balance_struct_name():
    return ACCOUNT_BALANCE_STRUCT_NAME


def sent_event_name():
    return SENT_EVENT_NAME


def received_event_name():
    return RECEIVED_EVENT_NAME


def account_struct_tag() -> StructTag:
    return StructTag(
        CORE_CODE_ADDRESS,
        ACCOUNT_MODULE_IDENTIFIER,
        ACCOUNT_STRUCT_NAME,
        [],
    )

def sent_payment_tag() -> StructTag:
    return StructTag (
        CORE_CODE_ADDRESS,
        ACCOUNT_MODULE_IDENTIFIER,
        SENT_EVENT_NAME,
        [],
    )

def received_payment_tag() -> StructTag:
    return StructTag (
        CORE_CODE_ADDRESS,
        ACCOUNT_MODULE_IDENTIFIER,
        RECEIVED_EVENT_NAME,
        [],
    )