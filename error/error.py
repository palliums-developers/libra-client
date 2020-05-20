from error.status_code import StatusCode
from lbrtypes.vm_error import StatusCode as LibraStatusCode

class ViolasError(Exception):
    def __init__(self, status_code, data=None, message=None):
        if status_code is None:
            status_code = StatusCode.UNKNOWN_STATUS
        status_code, message = self.handle_enum_code(status_code, message)
        # if isinstance(status_code, AdmissionControlStatusCode):
        #     status = f"ac_status:{status}"
        # elif isinstance(status_code, MempoolAddTransactionStatusCode):
        #     status = f"mem_status:{status}"
        super().__init__(status_code, data, message)


    @classmethod
    def from_response(cls, resp):
        code = resp.get("code")
        data = resp.get("data")
        message = resp.get("message")
        return cls(code, data, message)

    @property
    def code(self):
        '''
        Returns
        -------
        :class:`violas.error.status_code.StatusCode`
            status code of the error
        '''
        code, _ = self.args
        return code

    @property
    def msg(self):
        '''
        Returns
        -------
        str
            message of the error
        '''
        _, msg = self.args
        return msg

    @staticmethod
    def handle_enum_code(code, message):
        if not message:
            message = LibraStatusCode.get_name(code)
        return code, message

