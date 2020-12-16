import logging

from typing import Any
from fastapi_sqlalchemy import db
from fastapi import APIRouter, Depends

from app.models import User
from app.schemas.user import UserBase
from app.utils.paging import PaginationParams, paginate, Page

logger = logging.getLogger()
router = APIRouter()


@router.get("/", response_model=Page[UserBase])
def read_users(params: PaginationParams = Depends()) -> Any:
    try:
        users = paginate(db.session.query(User), params)
        return users
    except Exception as e:
        logger.error(e)
