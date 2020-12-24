import enum


class ExceptionType(enum.Enum):

    SALE_NOT_FOUND = 404, '404', 'Không tìm thấy nhân viên'
    STAFF_STATUS_INVALID = 400, '400', 'Trạng thái nhân viên không hợp lệ'

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, http_code, code, message):
        self.http_code = http_code
        self.code = code
        self.message = message
