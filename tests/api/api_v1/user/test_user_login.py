from starlette.testclient import TestClient

from app.core.config import settings
from app.core.security import get_password_hash
from app.models import User
from fastapi_sqlalchemy import db
from tests.api.api_v1 import APITestCase
from tests.faker import fake


class TestUser(APITestCase):
    ISSUE_KEY = "O2OSTAFF-244"

    def test_user_login(self, client: TestClient):
        """
            Test api user login success
            Step by step:
            - Khởi tạo data mẫu với password hash
            - Gọi API POST username/password
            - Đầu ra mong muốn:
                . status code: 200
                . access_token != null
                . token_type == 'bearer'
        """
        current_user: User = fake.user({'password': 'secret123'})
        r = client.post(f"{settings.API_PREFIX}/login", data={
            'username': current_user.email,
            'password': 'secret123'
        })
        assert r.status_code == 200
        response = r.json()
        assert response['access_token'] is not None
        assert response['token_type'] == 'bearer'

    def test_user_login_with_wrong_password(self, client: TestClient):
        """
            Test api user login with wrong password
            Step by step:
            - Khởi tạo data mẫu với password hash
            - Gọi API POST username/password nhưng sai password
            - Đầu ra mong muốn:
                . status code: 400
                . message == 'Incorrect email or password'
        """
        current_user: User = fake.user({'password': 'secret123'})
        r = client.post(f"{settings.API_PREFIX}/login", data={
            'username': current_user.email,
            'password': 'secret1234'    # khac voi password khoi tao User la secret123
        })
        assert r.status_code == 400
        response = r.json()
        assert response['code'] == '400'
        assert response['message'] == 'Incorrect email or password'

    def test_inactive_user_login(self, client: TestClient):
        """
            Test api user login with inactive user
            Step by step:
            - Khởi tạo data mẫu với password hash và is_active = False
            - Gọi API POST username/password
            - Đầu ra mong muốn:
                . status code: 400
                . message == 'Inactive user'
        """
        current_user: User = fake.user({'password': 'secret123', 'is_active': False})
        r = client.post(f"{settings.API_PREFIX}/login", data={
            'username': current_user.email,
            'password': 'secret123'
        })
        assert r.status_code == 400
        response = r.json()
        assert response['code'] == '400'
        assert response['message'] == 'Inactive user'
