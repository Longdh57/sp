from starlette.testclient import TestClient

from app.core.config import settings
from app.core.security import get_password_hash
from app.models import User
from fastapi_sqlalchemy import db
from tests.api.api_v1 import APITestCase


class TestUser(APITestCase):
    ISSUE_KEY = "O2OSTAFF-244"

    TEST_EMAIL = 'long.dh@teko.vn'
    TEST_PASSWORD = 'secret123'

    def setup_method(self):
        user = User(
            full_name='long dao',
            email=self.TEST_EMAIL,
            hashed_password=get_password_hash(self.TEST_PASSWORD),
            is_active=True,
            is_superuser=False
        )

        with db():
            db.session.bulk_save_objects([user])
            db.session.commit()

    def test_user_login(self, client: TestClient):
        """
            Test api user login
            Step by step:
            - Khởi tạo data mẫu với password hash
            - Gọi API POST username/password
            - Đầu ra mong muốn:
                . status code: 200
                . access_token != null
        """
        r = client.post(f"{settings.API_PREFIX}/login", data={
            'username': self.TEST_EMAIL,
            'password': self.TEST_PASSWORD
        })
        assert r.status_code == 200
        response = r.json()
        assert response['access_token'] is not None
