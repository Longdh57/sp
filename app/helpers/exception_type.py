import enum


class ExceptionType(enum.Enum):

    SaleNotFound = 404, "Sale not found!"
    SaleNotValid = 400, "Sale not valid!"

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, code, message):
        self.code = code
        self.message = message
