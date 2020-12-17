from typing import Optional, TypeVar, Generic
from pydantic.generics import GenericModel

from pydantic import BaseModel

T = TypeVar("T")


class ResponseSchemaBase(BaseModel):
    __abstract__ = True

    code: int = 200
    success: bool = True
    message: str = ""

    def custom_response(self, code: int, success: bool, message: str):
        self.code = code
        self.success = success
        self.message = message
        return self

    def success_response(self):
        self.message = 'success'
        return self

    def fail_response(self, code: int, message: str):
        self.code = code
        self.message = message
        return self

    def create_success_response(self):
        self.code = 201
        self.message = 'Create successful'
        return self


class DataResponse(ResponseSchemaBase, GenericModel, Generic[T]):
    data: Optional[T] = None

    class Config:
        arbitrary_types_allowed = True

    def custom_response(self, code: int, success: bool, message: str, data: T):
        self.code = code
        self.success = success
        self.message = message
        self.data = data
        return self

    def success_response(self, data: T):
        self.message = 'success'
        self.data = data
        return self

    def fail_response(self, code: int, message: str):
        self.code = code
        self.message = message
        self.data = None
        return self


class MetadataSchema(BaseModel):
    current_page: int
    page_size: int
    total_items: int
    next_page: Optional[int] = None
    previous_page: Optional[int] = None
    total_pages: int
