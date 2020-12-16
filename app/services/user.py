from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi_sqlalchemy import db
from pydantic import ValidationError

from app.core.config import settings
from app.core.security import verify_password
from app.models import User
from app.schemas.token import TokenPayload


class UserService(object):
    __instance = None

    reusable_oauth2 = OAuth2PasswordBearer(
        tokenUrl=f"{settings.API_PREFIX}/login"
    )

    @staticmethod
    def get_instance():
        """ Static access method. """
        if not UserService.__instance:
            UserService.__instance = UserService()
        return UserService.__instance

    def authenticate(self, *, email: str, password: str) -> Optional[User]:
        user = db.session.query(User).filter_by(email=email).first()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def get_current_user(self, token: str = Depends(reusable_oauth2)) -> User:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.SECURITY_ALGORITHM]
            )
            token_data = TokenPayload(**payload)
        except (jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )
        user = db.session.query(User).get(token_data.sub)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_current_active_user(self, current_user: User = Depends(get_current_user)) -> User:
        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
