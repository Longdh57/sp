from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.helpers.exception_type import ExceptionType
from app.schemas.base import ResponseSchemaBase


#   raise SaleServiceException(ExceptionType.SaleNotFound)
#   raise SaleServiceException(ExceptionType.SaleNotValid)
#   raise SaleServiceException(code=403, message="test exception")
class SaleServiceException(Exception):
    code: int
    message: str

    def __init__(self, exception_type: ExceptionType = None, code: int = None, message: str = None):
        if exception_type:
            self.code = exception_type.code
            self.message = exception_type.message
        else:
            self.code = code
            self.message = message


async def sale_service_exception_handler(request: Request, exc: SaleServiceException):
    return JSONResponse(
        status_code=exc.code,
        content=jsonable_encoder(ResponseSchemaBase().fail_response(exc.code, exc.message))
    )


async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(ResponseSchemaBase().fail_response(exc.status_code, exc.detail))
    )


async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder(ResponseSchemaBase().fail_response(400, get_message_validation(exc)))
    )


async def fastapi_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(ResponseSchemaBase().fail_response(500, "Có lỗi xảy ra, vui lòng liên hệ admin!"))
    )


def get_message_validation(exc):
    message = ""
    for error in exc.errors():
        message += "/'" + error.get("loc")[1] + "'/" + ': ' + error.get("msg") + ", "

    message = message[:-2]

    return message


