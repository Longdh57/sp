import logging

from typing import Any
from fastapi_sqlalchemy import db
from fastapi import APIRouter, Depends, HTTPException

from app.models import User
from app.schemas.user import UserBase
from app.services.user import UserService
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


@router.get("/me", response_model=UserBase)
def read_user_me(current_user: User = Depends(UserService.get_instance().get_current_user)) -> Any:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
