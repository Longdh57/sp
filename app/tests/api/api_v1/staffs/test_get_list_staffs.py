from app.core.config import settings
from app.models.staff import Staff
from app.helpers.enums import StaffStatus
from app.tests.conftest import TestClient
from fastapi_sqlalchemy import db
from app.tests.api.api_v1 import APITestCase


class TestStaff(APITestCase):
    ISSUE_KEY = "O2OSTAFF-246"

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

    def test_get_staff(self, client: TestClient):
        """
            Test get list nhân viên có phân trang với thông số mặc định
            Step by step:
            - Khởi tạo data mẫu gồm 2 nhân viên
                . {'id'= 1, 'staff_code': 'TEKO_01', 'full_name': 'Đinh Huy Bình', 'email': 'binh.dh@teko.vn', 'mobile': '0376752238', 'status': 1, 'alias': 'binh.dh'}
                . {'id'= 2', staff_code': 'TEKO_02', 'full_name': 'Đào Hải Long', 'email': 'longdh@teko.vn', 'mobile': '0123456789', 'status': 1, 'alias': 'longdh'}
            - Gọi API get list nhân viên với các thông số mặc định: ?size=15&page=0&sort_by=id&direction=desc
            - Đầu ra mong muốn:
                . status code: 200
                . total_items: 2
                . list nhân viên không null, không empty, size = 2 và nhân viên đầu tiên có email là 'longdh@teko.vn',
                 nhân viên thứ 2 có email là 'binh.dh@teko.vn'
        """
        r = client.get(f"{settings.API_PREFIX}/staffs/")
        assert r.status_code == 200
        staffs = r.json()
        assert staffs['total'] == 2
        assert staffs['items'] is not None and len(staffs['items']) == 2
        assert staffs['items'][0]['email'] == 'longdh@teko.vn' and staffs['items'][1]['email'] == 'binh.dh@teko.vn'

    def test_get_staff_invalid_page(self, client: TestClient):
        """
            Test get list nhân viên có phân trang với page không hợp lệ
            Step by step:
            - Khởi tạo data mẫu gồm 2 nhân viên
                . {'staff_code': 'TEKO_01', 'full_name': 'Đinh Huy Bình', 'email': 'binh.dh@teko.vn', 'mobile': '0376752238', 'status': 1, 'alias': 'binh.dh'}
                . {'staff_code': 'TEKO_02', 'full_name': 'Đào Hải Long', 'email': 'longdh@teko.vn', 'mobile': '0123456789', 'status': 1, 'alias': 'longdh'}
            - Gọi API get list nhân viên với page=1: ?size=15&page=1&sort_by=id&direction=desc
            - Đầu ra mong muốn:
                . status code: 200
                . total_items: 2
                . list nhân viên empty
        """
        r = client.get(f"{settings.API_PREFIX}/staffs/?size=15&page=1&sort_by=id&direction=desc")
        assert r.status_code == 200
        staffs = r.json()
        print(staffs)
        assert staffs['total'] == 2
        assert staffs['items'] is not None and len(staffs['items']) == 0

    def test_get_staff_search(self, client: TestClient):
        """
            Test get list nhân viên có phân trang với thông số filter by email
            Step by step:
            - Khởi tạo data mẫu gồm 2 nhân viên
                . {'staff_code': 'TEKO_01', 'full_name': 'Đinh Huy Bình', 'email': 'binh.dh@teko.vn', 'mobile': '0376752238', 'status': 1, 'alias': 'binh.dh'}
                . {'staff_code': 'TEKO_02', 'full_name': 'Đào Hải Long', 'email': 'longdh@teko.vn', 'mobile': '0123456789', 'status': 1, 'alias': 'longdh'}
            - Gọi API get list nhân viên với filter email=binh: ?size=15&page=0&sort_by=id&direction=desc&email=binh
            - Đầu ra mong muốn:
                . status code: 200
                . total_items: 1
                . list nhân viên không null và có size bằng 1, nhân viên đầu tiên có email là 'binh.dh@teko.vn'
        """
        r = client.get(f"{settings.API_PREFIX}/staffs/?size=15&page=0&sort_by=id&direction=desc&email=binh")
        assert r.status_code == 200
        staffs = r.json()
        print(staffs)
        assert staffs['total'] == 1
        assert staffs['items'] is not None and len(staffs['items']) == 1 and staffs['items'][0]['email'] == 'binh.dh@teko.vn'

    def test_invalid_sort_by(self, client: TestClient):
        """
            Test get list nhân viên có phân trang với thông số sort_by không hợp lệ
            Step by step:
            - Khởi tạo data mẫu gồm 2 nhân viên
                . {'staff_code': 'TEKO_01', 'full_name': 'Đinh Huy Bình', 'email': 'binh.dh@teko.vn', 'mobile': '0376752238', 'status': 1, 'alias': 'binh.dh'}
                . {'staff_code': 'TEKO_02', 'full_name': 'Đào Hải Long', 'email': 'longdh@teko.vn', 'mobile': '0123456789', 'status': 1, 'alias': 'longdh'}
            - Gọi API get list nhân viên với params sort_by không hợp lệ: ?size=15&page=0&sort_by=new_field&direction=desc
            - Đầu ra mong muốn:
                . status code: 500
                . message: type object 'Staff' has no attribute 'new_field'
        """
        r = client.get(f"{settings.API_PREFIX}/staffs/?size=15&page=0&sort_by=new_field&direction=desc")
        assert r.status_code == 500
        staffs = r.json()
        print(staffs)
        assert staffs['message'] == "type object 'Staff' has no attribute 'new_field'"

