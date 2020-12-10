from typing import Optional

from pydantic import BaseModel


class ResponseSchemaBase(BaseModel):
    __abstract__ = True

    code: int = 200
    success: bool = True
    message: str = ""


class MetadataSchema(BaseModel):
    current_page: int
    page_size: int
    total_items: int
    next_page: Optional[int] = None
    previous_page: Optional[int] = None
    total_pages: int
