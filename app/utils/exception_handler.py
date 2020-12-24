from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.helpers.exception_type import ExceptionType
from app.schemas.base import ResponseSchemaBase


#   raise SaleServiceException(ExceptionType.SaleNotFound)
#   raise SaleServiceException(http_code=400, code='400', message="test exception")
class SaleServiceException(Exception):
    http_code: int
    code: str
    message: str

    def __init__(self, exception_type: ExceptionType = None, http_code: int = None, code: str = None, message: str = None):
        if exception_type:
            self.http_code = exception_type.http_code
            self.code = exception_type.code
            self.message = exception_type.message
        else:
            self.http_code = http_code if http_code else 500
            self.code = code if code else str(self.http_code)
            self.message = message


async def sale_service_exception_handler(request: Request, exc: SaleServiceException):
    return JSONResponse(
        status_code=exc.http_code,
        content=jsonable_encoder(ResponseSchemaBase().custom_response(exc.code, exc.message))
    )


async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(ResponseSchemaBase().custom_response(str(exc.status_code), exc.detail))
    )


async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder(ResponseSchemaBase().custom_response('400', get_message_validation(exc)))
    )


async def fastapi_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(ResponseSchemaBase().custom_response('500', "Có lỗi xảy ra, vui lòng liên hệ admin!"))
    )


def get_message_validation(exc):
    message = ""
    for error in exc.errors():
        message += "/'" + error.get("loc")[1] + "'/" + ': ' + error.get("msg") + ", "

    message = message[:-2]

    return message


