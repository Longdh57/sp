from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app import models
from app.core.config import settings
from app.schemas.base import DataResponse
from app.schemas.token import Token
from app.schemas.user import User
from app.services.user import UserService
from app.core.security import get_password_hash, create_access_token

router = APIRouter()


@router.post("/login", response_model=DataResponse[Token])
def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = UserService.get_instance().authenticate(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail='Incorrect email or password')
    elif not user.is_active:
        raise HTTPException(status_code=400, detail='Inactive user')
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return DataResponse().success_response({
        "access_token": create_access_token(user.id, expires_delta=access_token_expires)
    })


@router.post("/login/test-token", response_model=DataResponse[User])
def test_token(current_user: models.User = Depends(UserService.get_instance().get_current_user)) -> Any:
    return DataResponse().success_response({current_user})


@router.post("/login/get-password-hash")
def get_password(passsword: str):
    return get_password_hash(passsword)
