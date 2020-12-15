import logging
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import Optional, Generic, Sequence, Type, TypeVar
from sqlalchemy.orm import Query
from pydantic.generics import GenericModel
from contextvars import ContextVar
from app.schemas.base import ResponseSchemaBase, MetadataSchema


T = TypeVar("T")
C = TypeVar("C")

logger = logging.getLogger()


class PaginationParams(BaseModel):
    size: Optional[int] = 15
    page: Optional[int] = 0
    sort_by: Optional[str] = 'id'
    direction: Optional[str] = 'desc'


class BasePage(ResponseSchemaBase, GenericModel, Generic[T], ABC):
    total: int = Field(..., ge=0)
    items: Sequence[T]

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    @abstractmethod
    def create(cls: Type[C], code: int, success: bool, message: str, total: int,
               items: Sequence[T], metadata: MetadataSchema) -> C:
        pass  # pragma: no cover


class Page(BasePage[T], Generic[T]):
    metadata: MetadataSchema

    @classmethod
    def create(cls, code: int, success: bool, message: str, total: int,
               items: Sequence[T], metadata: MetadataSchema) -> "Page[T]":
        return cls(
            code=code,
            success=success,
            message=message,
            total=total,
            items=items,
            metadata=metadata
        )


PageType: ContextVar[Type[BasePage]] = ContextVar("PageType", default=Page)


def paginate(query: Query, params: Optional[PaginationParams] = None) -> BasePage:
    code = 200
    success = True
    message = ""

    try:
        total = query.count()
        items = query.limit(params.size).offset(params.size*params.page).all()

        total_page = total // params.size + 1 if total % params.size != 0 else total // params.size
        metadata = MetadataSchema(
            current_page=params.page,
            page_size=params.size,
            total_items=total,
            next_page=None if params.page + 1 >= total_page else params.page + 1,
            previous_page=None if params.page <= 0 else params.page - 1,
            total_pages=total_page
            # last_page=total_page - 1 if total_page > 0 else 0
        )

    except Exception as e:
        code = 500
        success = False
        message = str(e)
        items = None
        total = 0
        metadata = None
        logger.error("Error when execute query: {}".format(e))

    return PageType.get().create(code, success, message, total, items, metadata)
