from app.core.config import settings
from app.models.staff import Staff
from app.helpers.enums import StaffStatus
from tests.conftest import TestClient
from fastapi_sqlalchemy import db
from tests.api.api_v1 import APITestCase


class TestStaff(APITestCase):
    ISSUE_KEY = "O2OSTAFF-239"

    def setup_method(self):
        staff_db1 = Staff(
            staff_code='TEKO_01',
            full_name='Đinh Huy Bình',
            email='binh.dh@teko.vn',
            mobile='0376752238',
            is_superuser=True,
            alias='binh.dh',
            status=StaffStatus.ACTIVE
        )
        staff_db2 = Staff(
            staff_code='TEKO_02',
            full_name='Đào Hải Long',
            email='longdh@teko.vn',
            mobile='0123456789',
            is_superuser=False,
            alias='longdh',
            status=StaffStatus.ACTIVE
        )
        with db():
            db.session.bulk_save_objects([staff_db1, staff_db2])
            db.session.commit()

    def test_update_staff(self, client: TestClient):
        """
            Test update thông tin nhân viên
            Step by step:
            - Khởi tạo data mẫu gồm 2 nhân viên
                . {'id'= 1, 'staff_code': 'TEKO_01', 'full_name': 'Đinh Huy Bình', 'email': 'binh.dh@teko.vn', 'mobile': '0376752238', 'status': 1, 'alias': 'binh.dh'}
                . {'id'= 2', staff_code': 'TEKO_02', 'full_name': 'Đào Hải Long', 'email': 'longdh@teko.vn', 'mobile': '0123456789', 'status': 1, 'alias': 'longdh'}
            - Gọi API updtate nhân viên số 2 với các thông số: staff_id = 2
                {
                    "status": -1,
                    "alias": "long_teko"
                }
            - Đầu ra mong muốn:
                . status code: 200
                . code: '000'
                . get staff với id = 2, kiểm tra trạng thái mong muốn là DISABLE và alias mong muốn là 'long_teko'
        """

        body = {
            "status": -1,
            "alias": "long_teko"
        }
        r = client.put(f"{settings.API_PREFIX}/staffs/2", json=body)
        assert r.status_code == 200
        response = r.json()
        assert response['code'] == '000'

        with db():
            staff = db.session.query(Staff).filter_by(id=2).first()
            assert staff is not None
            assert staff.status == StaffStatus.DISABLE and staff.alias == 'long_teko'

    def test_staff_not_found(self, client: TestClient):
        """
            Test update thông tin nhân viên với nhân viên không có trong database
            Step by step:
            - Khởi tạo data mẫu gồm 2 nhân viên
                . {'id'= 1, 'staff_code': 'TEKO_01', 'full_name': 'Đinh Huy Bình', 'email': 'binh.dh@teko.vn', 'mobile': '0376752238', 'status': 1, 'alias': 'binh.dh'}
                . {'id'= 2', staff_code': 'TEKO_02', 'full_name': 'Đào Hải Long', 'email': 'longdh@teko.vn', 'mobile': '0123456789', 'status': 1, 'alias': 'longdh'}
            - Gọi API updtate nhân viên số 3 với các thông số: staff_id = 3
                {
                    "status": -1,
                    "alias": "new_user"
                }
            - Đầu ra mong muốn:
                . status code: 404
                . message: 'Không tìm thấy nhân viên'
        """

        body = {
            "status": -1,
            "alias": "new_user"
        }
        r = client.put(f"{settings.API_PREFIX}/staffs/3", json=body)
        assert r.status_code == 404
        response = r.json()
        assert response['message'] == 'Không tìm thấy nhân viên'

    def test_update_missing_params(self, client: TestClient):
        """
            Test update thông tin nhân viên với body thiếu thông tin status
            Step by step:
            - Khởi tạo data mẫu gồm 2 nhân viên
                . {'id'= 1, 'staff_code': 'TEKO_01', 'full_name': 'Đinh Huy Bình', 'email': 'binh.dh@teko.vn', 'mobile': '0376752238', 'status': 1, 'alias': 'binh.dh'}
                . {'id'= 2', staff_code': 'TEKO_02', 'full_name': 'Đào Hải Long', 'email': 'longdh@teko.vn', 'mobile': '0123456789', 'status': 1, 'alias': 'longdh'}
             - Gọi API updtate nhân viên số 2 với các thông số: staff_id = 2
                {
                    "alias": "new_user"
                }
            - Đầu ra mong muốn:
                . status code: 400
                . message: "/'status'/: field required"
        """

        body = {
            "alias": "long_teko"
        }
        r = client.put(f"{settings.API_PREFIX}/staffs/2", json=body)
        assert r.status_code == 400
        response = r.json()
        assert response['message'] == "/'status'/: field required"

    def test_update_invalid_params(self, client: TestClient):
        """
            Test update thông tin nhân viên với body bị sai định dạng (status không hợp lệ)
            Step by step:
            - Khởi tạo data mẫu gồm 2 nhân viên
                . {'id'= 1, 'staff_code': 'TEKO_01', 'full_name': 'Đinh Huy Bình', 'email': 'binh.dh@teko.vn', 'mobile': '0376752238', 'status': 1, 'alias': 'binh.dh'}
                . {'id'= 2', staff_code': 'TEKO_02', 'full_name': 'Đào Hải Long', 'email': 'longdh@teko.vn', 'mobile': '0123456789', 'status': 1, 'alias': 'longdh'}
             - Gọi API updtate nhân viên số 2 với các thông số: staff_id = 2
                {
                    "status": 0,
                    "alias": "new_user"
                }
            - Đầu ra mong muốn:
                . status code: 400
                . message: 'Trạng thái nhân viên không hợp lệ'
        """

        body = {
            "status": 0,
            "alias": "long_teko"
        }
        r = client.put(f"{settings.API_PREFIX}/staffs/2", json=body)
        assert r.status_code == 400
        response = r.json()
        assert response['message'] == 'Trạng thái nhân viên không hợp lệ'

    def test_update_invalid_format_params(self, client: TestClient):
        """
            Test update thông tin nhân viên với body bị sai định dạng (status không đúng định dạng)
            Step by step:
            - Khởi tạo data mẫu gồm 2 nhân viên
                . {'id'= 1, 'staff_code': 'TEKO_01', 'full_name': 'Đinh Huy Bình', 'email': 'binh.dh@teko.vn', 'mobile': '0376752238', 'status': 1, 'alias': 'binh.dh'}
                . {'id'= 2', staff_code': 'TEKO_02', 'full_name': 'Đào Hải Long', 'email': 'longdh@teko.vn', 'mobile': '0123456789', 'status': 1, 'alias': 'longdh'}
             - Gọi API updtate nhân viên số 2 với các thông số: staff_id = 2
                {
                    "status": "str_status",
                    "alias": "new_user"
                }
            - Đầu ra mong muốn:
                . status code: 400
                . message: "/'status'/: value is not a valid integer"
        """

        body = {
            "status": "str_status",
            "alias": "long_teko"
        }
        r = client.put(f"{settings.API_PREFIX}/staffs/2", json=body)
        assert r.status_code == 400
        response = r.json()
        assert response['message'] == "/'status'/: value is not a valid integer"

