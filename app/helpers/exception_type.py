import enum


class ExceptionType(enum.Enum):

    SaleNotFound = 404, '404', 'Sale not found!'
    StaffStatusInvalid = 400, '400', 'Trạng thái nhân viên không hợp lệ'

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, http_code, code, message):
        self.http_code = http_code
        self.code = code
        self.message = message
