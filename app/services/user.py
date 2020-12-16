from typing import Optional

from fastapi_sqlalchemy import db

from app.core.security import verify_password
from app.models import User


class UserService(object):
    __instance = None

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
