from app.core.config import settings
from app.models.staff import Staff
from app.helpers.enums import StaffStatus
from app.tests.conftest import TestClient
from fastapi_sqlalchemy import db
from app.tests.api.api_v1 import APITestCase


class TestStaff(APITestCase):
    ISSUE_KEY = "O2OSTAFF-241"

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
            full_name='Nguyễn Văn A',
            email='a.teko@teko.vn',
            mobile='0111111111',
            is_superuser=False,
            alias='user_a',
            status=StaffStatus.ACTIVE,
            parent_id=1
        )
        staff_db3 = Staff(
            staff_code='TEKO_03',
            full_name='Nguyễn Văn B',
            email='b.teko@teko.vn',
            mobile='0111111122',
            is_superuser=False,
            alias='user_b',
            status=StaffStatus.ACTIVE,
            parent_id=1
        )
        with db():
            db.session.bulk_save_objects([staff_db1, staff_db2, staff_db3])
            db.session.commit()

    def test_get_staff(self, client: TestClient):
        """
            Test get list nhân viên có phân trang.
            Step by step:
            - Khởi tạo data mẫu gồm 2 nhân viên
                . {'staff_code': 'TEKO_01', 'full_name': 'Đinh Huy Bình', 'email': 'binh.dh@teko.vn', 'mobile': '0376752238', 'status': 1, 'alias': 'binh.dh'}
                . {'staff_code': 'TEKO_02', 'full_name': 'Đào Hải Long', 'email': 'longdhh@teko.vn', 'mobile': '0123456789', 'status': 1, 'alias': 'longdh'}
            - Gọi API get list nhân viên
            - Đầu ra mong muốn:
                . status code: 200
                . total_item: 2
                . list nhân viên không null, không empty, size = 2 và nhân viên đầu tiên có email là 'binh.dh@teko.vn',
                 nhân viên thứ 2 có email là 'longdh@teko.vn'
        """
        r = client.get(f"{settings.API_PREFIX}/staffs/1/staff-children")
        assert r.status_code == 200
        staffs = r.json()
        print(staffs)
        assert staffs['data'] is not None and len(staffs['data']) == 3
        assert staffs['data'][0]['email'] == 'binh.dh@teko.vn'

