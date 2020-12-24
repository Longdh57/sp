import logging
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import Optional, Generic, Sequence, Type, TypeVar

from sqlalchemy import asc, desc
from sqlalchemy.orm import Query
from pydantic.generics import GenericModel
from contextvars import ContextVar

from app.models import Staff
from app.schemas.base import ResponseSchemaBase, MetadataSchema
from app.utils.exception_handler import SaleServiceException

T = TypeVar("T")
C = TypeVar("C")

logger = logging.getLogger()


class PaginationParams(BaseModel):
    size: Optional[int] = 15
    page: Optional[int] = 0
    sort_by: Optional[str] = 'id'
    direction: Optional[str] = 'desc'


class BasePage(ResponseSchemaBase, GenericModel, Generic[T], ABC):
    data: Sequence[T]

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    @abstractmethod
    def create(cls: Type[C], code: str, message: str, data: Sequence[T], metadata: MetadataSchema) -> C:
        pass  # pragma: no cover


class Page(BasePage[T], Generic[T]):
    metadata: MetadataSchema

    @classmethod
    def create(cls, code: str, message: str, data: Sequence[T], metadata: MetadataSchema) -> "Page[T]":
        return cls(
            code=code,
            message=message,
            data=data,
            metadata=metadata
        )


PageType: ContextVar[Type[BasePage]] = ContextVar("PageType", default=Page)


def paginate(query: Query, params: Optional[PaginationParams] = None) -> BasePage:
    code = '000'
    message = ''

    try:
        total = query.count()
        if params.direction:
            direction = desc if params.direction == 'desc' else asc
            data = query.order_by(direction(getattr(Staff, params.sort_by))) \
                .limit(params.size).offset(params.size * params.page)\
                .all()
        else:
            data = query.limit(params.size).offset(params.size * params.page).all()

        metadata = MetadataSchema(
            current_page=params.page,
            page_size=params.size,
            total_items=total
        )

    except Exception as e:
        raise SaleServiceException(http_code=500, code='500', message=str(e))

    return PageType.get().create(code, message, data, metadata)
