from typing import Optional

from pydantic import BaseModel


class ResponseSchemaBase(BaseModel):
    __abstract__ = True

    code: int = 200
    success: bool = True
    message: str = ""

    def custom_response(self, code: int, success: bool, message: str):
        self.code = code
        self.success = success
        self.message = message

    def success_response(self, message: str):
        self.message = 'success'

    def fail_response(self, code: int, message: str):
        self.code = code
        self.message = message

    def create_success_response(self):
        self.code = 201
        self.message = 'Create successful'


class MetadataSchema(BaseModel):
    current_page: int
    page_size: int
    total_items: int
    next_page: Optional[int] = None
    previous_page: Optional[int] = None
    total_pages: int
