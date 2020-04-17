from enum import IntEnum
from libra.vm_error import StatusCode as LibraStatusCode

class StatusCode(IntEnum):
    FETCH_ERROR_MESSAGE = 10001
    WAIT_TRANSACTION_TIME_OUT = 10002
    ENSURE_ERROR = 10003