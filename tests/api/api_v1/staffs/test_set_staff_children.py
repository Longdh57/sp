from app.core.config import settings
from app.models.staff import Staff
from app.helpers.enums import StaffStatus
from tests.conftest import TestClient
from fastapi_sqlalchemy import db
from tests.api.api_v1 import APITestCase


class TestStaff(APITestCase):
    ISSUE_KEY = "O2OSTAFF-240"

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
        staff_db4 = Staff(
            staff_code='TEKO_04',
            full_name='Nguyễn Văn C',
            email='c.teko@teko.vn',
            mobile='0111111133',
            is_superuser=False,
            alias='user_c',
            status=StaffStatus.ACTIVE,
            parent_id=2
        )
        staff_db5 = Staff(
            staff_code='TEKO_05',
            full_name='Nguyễn Văn D',
            email='d.teko@teko.vn',
            mobile='0111111144',
            is_superuser=False,
            alias='user_d',
            status=StaffStatus.ACTIVE,
            parent_id=3
        )
        staff_db6 = Staff(
            staff_code='TEKO_06',
            full_name='Nguyễn Văn E',
            email='e.teko@teko.vn',
            mobile='0111111155',
            is_superuser=False,
            alias='user_e',
            status=StaffStatus.ACTIVE,
            parent_id=4
        )
        staff_db7 = Staff(
            staff_code='TEKO_07',
            full_name='Nguyễn Văn G',
            email='g.teko@teko.vn',
            mobile='0111111166',
            is_superuser=False,
            alias='user_g',
            status=StaffStatus.ACTIVE,
        )
        staff_db8 = Staff(
            staff_code='TEKO_08',
            full_name='Nguyễn Văn H',
            email='h.teko@teko.vn',
            mobile='0111111177',
            is_superuser=False,
            alias='user_h',
            status=StaffStatus.ACTIVE,
            parent_id=7
        )
        with db():
            db.session.bulk_save_objects([staff_db1, staff_db2, staff_db3, staff_db4,
                                          staff_db5, staff_db6, staff_db7, staff_db8])
            db.session.commit()

    def test_set_children_success(self, client: TestClient):
        """
            Test api set list children
            Step by step:
            - Khởi tạo data mẫu gồm 8 nhân viên
                . {'id'= 1, 'staff_code': 'TEKO_01', 'full_name': 'Đinh Huy Bình', 'email': 'binh.dh@teko.vn', 'mobile': '0376752238', 'status': 1, 'alias': 'binh.dh', 'parent_id': null}
                . {'id'= 2', staff_code': 'TEKO_02', 'full_name': 'Nguyễn Văn A', 'email': 'a.teko@teko.vn', 'mobile': '0111111111', 'status': 1, 'alias': 'user_a', 'parent_id': 1}
                . {'id'= 3', staff_code': 'TEKO_03', 'full_name': 'Nguyễn Văn B', 'email': 'b.teko@teko.vn', 'mobile': '0111111122', 'status': 1, 'alias': 'user_b', 'parent_id': 1}
                . {'id'= 4', staff_code': 'TEKO_04', 'full_name': 'Nguyễn Văn C', 'email': 'c.teko@teko.vn', 'mobile': '0111111133', 'status': 1, 'alias': 'user_c', 'parent_id': 2}
                . {'id'= 5', staff_code': 'TEKO_05', 'full_name': 'Nguyễn Văn D', 'email': 'd.teko@teko.vn', 'mobile': '0111111144', 'status': 1, 'alias': 'user_d', 'parent_id': 3}
                . {'id'= 6', staff_code': 'TEKO_06', 'full_name': 'Nguyễn Văn E', 'email': 'e.teko@teko.vn', 'mobile': '0111111155', 'status': 1, 'alias': 'user_e', 'parent_id': 4}
                . {'id'= 7', staff_code': 'TEKO_07', 'full_name': 'Nguyễn Văn G', 'email': 'g.teko@teko.vn', 'mobile': '0111111166', 'status': 1, 'alias': 'user_g', 'parent_id': null}
                . {'id'= 8', staff_code': 'TEKO_08', 'full_name': 'Nguyễn Văn H', 'email': 'h.teko@teko.vn', 'mobile': '0111111177', 'status': 1, 'alias': 'user_h', 'parent_id': 7}
            - Gọi API set danh sách nhân viên cấp dưới cho user1: id = 1
                . API: ../sale-service/staffs/1/staff-children, method put
                . body:
                    {
                        [3,4,5]
                    }
            - Đầu ra mong muốn:
                . status code: 200
                . code: '000'

                . get cây phân quyền của user 1 sẽ có 4 node
                    . node1: user2, id=2, email = a.teko@teko.vn ( node lá)
                    . node2: user3, id=3, email = b.teko@teko.vn (node lá)
                    . node3: user4, id=4, email = c.teko@teko.vn
                        . trong node3 có 1 node3.1 là user6, id=6, email = e.teko@teko.vn (node lá)
                    . node4: user5, id=5, email = d.teko@teko.vn (node lá)
        """

        body = [3, 4, 5]
        r = client.put(f"{settings.API_PREFIX}/staffs/1/staff-children", json=body)
        assert r.status_code == 200
        response = r.json()
        assert response['code'] == '000'

        r = client.get(f"{settings.API_PREFIX}/staffs/1/staff-children-tree")
        assert r.status_code == 200
        response = r.json()
        assert response['code'] == '000'

        assert response['data'] is not None and response['data'] != {}
        assert response['data']['id'] == 1 and response['data']['email'] == 'binh.dh@teko.vn'
        assert response['data']['children'] is not None and len(response['data']['children']) == 4

        node1 = response['data']['children'][0]
        node2 = response['data']['children'][1]
        node3 = response['data']['children'][2]
        node4 = response['data']['children'][3]

        assert node1['id'] == 2 and node1['email'] == 'a.teko@teko.vn'
        assert node2['id'] == 3 and node2['email'] == 'b.teko@teko.vn'
        assert node3['id'] == 4 and node3['email'] == 'c.teko@teko.vn'
        assert node4['id'] == 5 and node4['email'] == 'd.teko@teko.vn'

        assert node1['children'] is not None and len(node1['children']) == 0
        assert node2['children'] is not None and len(node2['children']) == 0
        assert node3['children'] is not None and len(node3['children']) == 1
        assert node4['children'] is not None and len(node4['children']) == 0

        node31 = node3['children'][0]
        assert node31['id'] == 6 and node31['email'] == 'e.teko@teko.vn'
        assert node31['children'] is not None and len(node31['children']) == 0

    def test_parent_not_found(self, client: TestClient):
        """
            Test api set list children với staff_id không có trong databse
            Step by step:
            - Khởi tạo data mẫu gồm 8 nhân viên
                . {'id'= 1, 'staff_code': 'TEKO_01', 'full_name': 'Đinh Huy Bình', 'email': 'binh.dh@teko.vn', 'mobile': '0376752238', 'status': 1, 'alias': 'binh.dh', 'parent_id': null}
                . {'id'= 2', staff_code': 'TEKO_02', 'full_name': 'Nguyễn Văn A', 'email': 'a.teko@teko.vn', 'mobile': '0111111111', 'status': 1, 'alias': 'user_a', 'parent_id': 1}
                . {'id'= 3', staff_code': 'TEKO_03', 'full_name': 'Nguyễn Văn B', 'email': 'b.teko@teko.vn', 'mobile': '0111111122', 'status': 1, 'alias': 'user_b', 'parent_id': 1}
                . {'id'= 4', staff_code': 'TEKO_04', 'full_name': 'Nguyễn Văn C', 'email': 'c.teko@teko.vn', 'mobile': '0111111133', 'status': 1, 'alias': 'user_c', 'parent_id': 2}
                . {'id'= 5', staff_code': 'TEKO_05', 'full_name': 'Nguyễn Văn D', 'email': 'd.teko@teko.vn', 'mobile': '0111111144', 'status': 1, 'alias': 'user_d', 'parent_id': 3}
                . {'id'= 6', staff_code': 'TEKO_06', 'full_name': 'Nguyễn Văn E', 'email': 'e.teko@teko.vn', 'mobile': '0111111155', 'status': 1, 'alias': 'user_e', 'parent_id': 4}
                . {'id'= 7', staff_code': 'TEKO_07', 'full_name': 'Nguyễn Văn G', 'email': 'g.teko@teko.vn', 'mobile': '0111111166', 'status': 1, 'alias': 'user_g', 'parent_id': null}
                . {'id'= 8', staff_code': 'TEKO_08', 'full_name': 'Nguyễn Văn H', 'email': 'h.teko@teko.vn', 'mobile': '0111111177', 'status': 1, 'alias': 'user_h', 'parent_id': 7}
            - Gọi API set danh sách nhân viên cấp dưới cho user9: id = 9
                . API: ../sale-service/staffs/9/staff-children, method put
                . body:
                    {
                        [3,4,5]
                    }
            - Đầu ra mong muốn:
                . status code: 404
                . code: 'Không tìm thấy nhân viên'
        """

        body = [3, 4, 5]
        r = client.put(f"{settings.API_PREFIX}/staffs/9/staff-children", json=body)
        assert r.status_code == 404
        response = r.json()
        assert response['message'] == 'Không tìm thấy nhân viên'

    def test_list_children_empty(self, client: TestClient):
        """
            Test api set list children với list child_id rỗng []
            Step by step:
            - Khởi tạo data mẫu gồm 8 nhân viên
                . {'id'= 1, 'staff_code': 'TEKO_01', 'full_name': 'Đinh Huy Bình', 'email': 'binh.dh@teko.vn', 'mobile': '0376752238', 'status': 1, 'alias': 'binh.dh', 'parent_id': null}
                . {'id'= 2', staff_code': 'TEKO_02', 'full_name': 'Nguyễn Văn A', 'email': 'a.teko@teko.vn', 'mobile': '0111111111', 'status': 1, 'alias': 'user_a', 'parent_id': 1}
                . {'id'= 3', staff_code': 'TEKO_03', 'full_name': 'Nguyễn Văn B', 'email': 'b.teko@teko.vn', 'mobile': '0111111122', 'status': 1, 'alias': 'user_b', 'parent_id': 1}
                . {'id'= 4', staff_code': 'TEKO_04', 'full_name': 'Nguyễn Văn C', 'email': 'c.teko@teko.vn', 'mobile': '0111111133', 'status': 1, 'alias': 'user_c', 'parent_id': 2}
                . {'id'= 5', staff_code': 'TEKO_05', 'full_name': 'Nguyễn Văn D', 'email': 'd.teko@teko.vn', 'mobile': '0111111144', 'status': 1, 'alias': 'user_d', 'parent_id': 3}
                . {'id'= 6', staff_code': 'TEKO_06', 'full_name': 'Nguyễn Văn E', 'email': 'e.teko@teko.vn', 'mobile': '0111111155', 'status': 1, 'alias': 'user_e', 'parent_id': 4}
                . {'id'= 7', staff_code': 'TEKO_07', 'full_name': 'Nguyễn Văn G', 'email': 'g.teko@teko.vn', 'mobile': '0111111166', 'status': 1, 'alias': 'user_g', 'parent_id': null}
                . {'id'= 8', staff_code': 'TEKO_08', 'full_name': 'Nguyễn Văn H', 'email': 'h.teko@teko.vn', 'mobile': '0111111177', 'status': 1, 'alias': 'user_h', 'parent_id': 7}
            - Gọi API set danh sách nhân viên cấp dưới cho user1: id = 1
                . API: ../sale-service/staffs/1/staff-children, method put
                . body:
                    {
                        []
                    }
            - Đầu ra mong muốn:
                . status code: 400
                . code: 'Danh sách nhân viên cấp dưới không được rỗng'
        """

        body = []
        r = client.put(f"{settings.API_PREFIX}/staffs/1/staff-children", json=body)
        assert r.status_code == 400
        response = r.json()
        assert response['message'] == 'Danh sách nhân viên cấp dưới không được rỗng'

    def test_list_children_invalid(self, client: TestClient):
        """
            Test api set list children với list child_id không thỏa mãn (có ít nhát 1 child_id không có trong database
             hoặc có ít nhất 2 child_id bị trùng nhau)
            Step by step:
            - Khởi tạo data mẫu gồm 8 nhân viên
                . {'id'= 1, 'staff_code': 'TEKO_01', 'full_name': 'Đinh Huy Bình', 'email': 'binh.dh@teko.vn', 'mobile': '0376752238', 'status': 1, 'alias': 'binh.dh', 'parent_id': null}
                . {'id'= 2', staff_code': 'TEKO_02', 'full_name': 'Nguyễn Văn A', 'email': 'a.teko@teko.vn', 'mobile': '0111111111', 'status': 1, 'alias': 'user_a', 'parent_id': 1}
                . {'id'= 3', staff_code': 'TEKO_03', 'full_name': 'Nguyễn Văn B', 'email': 'b.teko@teko.vn', 'mobile': '0111111122', 'status': 1, 'alias': 'user_b', 'parent_id': 1}
                . {'id'= 4', staff_code': 'TEKO_04', 'full_name': 'Nguyễn Văn C', 'email': 'c.teko@teko.vn', 'mobile': '0111111133', 'status': 1, 'alias': 'user_c', 'parent_id': 2}
                . {'id'= 5', staff_code': 'TEKO_05', 'full_name': 'Nguyễn Văn D', 'email': 'd.teko@teko.vn', 'mobile': '0111111144', 'status': 1, 'alias': 'user_d', 'parent_id': 3}
                . {'id'= 6', staff_code': 'TEKO_06', 'full_name': 'Nguyễn Văn E', 'email': 'e.teko@teko.vn', 'mobile': '0111111155', 'status': 1, 'alias': 'user_e', 'parent_id': 4}
                . {'id'= 7', staff_code': 'TEKO_07', 'full_name': 'Nguyễn Văn G', 'email': 'g.teko@teko.vn', 'mobile': '0111111166', 'status': 1, 'alias': 'user_g', 'parent_id': null}
                . {'id'= 8', staff_code': 'TEKO_08', 'full_name': 'Nguyễn Văn H', 'email': 'h.teko@teko.vn', 'mobile': '0111111177', 'status': 1, 'alias': 'user_h', 'parent_id': 7}
            - Gọi API set danh sách nhân viên cấp dưới cho user1: id = 1
                . API: ../sale-service/staffs/1/staff-children, method put
                . body:
                    {
                        [2,3,4,9]
                    }
            - Đầu ra mong muốn:
                . status code: 404
                . code: 'Không tìm thấy 1 hoặc nhiều nhân viên cấp dưới'
        """

        body = [2, 3, 4, 9]
        r = client.put(f"{settings.API_PREFIX}/staffs/1/staff-children", json=body)
        assert r.status_code == 404
        response = r.json()
        assert response['message'] == 'Không tìm thấy 1 hoặc nhiều nhân viên cấp dưới'

    def test_list_children_infinity_loop(self, client: TestClient):
        """
            Test api set list children với list child_id tạo thành chu trình lặp vô hạn
            Step by step:
            - Khởi tạo data mẫu gồm 8 nhân viên
                . {'id'= 1, 'staff_code': 'TEKO_01', 'full_name': 'Đinh Huy Bình', 'email': 'binh.dh@teko.vn', 'mobile': '0376752238', 'status': 1, 'alias': 'binh.dh', 'parent_id': null}
                . {'id'= 2', staff_code': 'TEKO_02', 'full_name': 'Nguyễn Văn A', 'email': 'a.teko@teko.vn', 'mobile': '0111111111', 'status': 1, 'alias': 'user_a', 'parent_id': 1}
                . {'id'= 3', staff_code': 'TEKO_03', 'full_name': 'Nguyễn Văn B', 'email': 'b.teko@teko.vn', 'mobile': '0111111122', 'status': 1, 'alias': 'user_b', 'parent_id': 1}
                . {'id'= 4', staff_code': 'TEKO_04', 'full_name': 'Nguyễn Văn C', 'email': 'c.teko@teko.vn', 'mobile': '0111111133', 'status': 1, 'alias': 'user_c', 'parent_id': 2}
                . {'id'= 5', staff_code': 'TEKO_05', 'full_name': 'Nguyễn Văn D', 'email': 'd.teko@teko.vn', 'mobile': '0111111144', 'status': 1, 'alias': 'user_d', 'parent_id': 3}
                . {'id'= 6', staff_code': 'TEKO_06', 'full_name': 'Nguyễn Văn E', 'email': 'e.teko@teko.vn', 'mobile': '0111111155', 'status': 1, 'alias': 'user_e', 'parent_id': 4}
                . {'id'= 7', staff_code': 'TEKO_07', 'full_name': 'Nguyễn Văn G', 'email': 'g.teko@teko.vn', 'mobile': '0111111166', 'status': 1, 'alias': 'user_g', 'parent_id': null}
                . {'id'= 8', staff_code': 'TEKO_08', 'full_name': 'Nguyễn Văn H', 'email': 'h.teko@teko.vn', 'mobile': '0111111177', 'status': 1, 'alias': 'user_h', 'parent_id': 7}
            - Gọi API set danh sách nhân viên cấp dưới cho user6: id = 6
                . API: ../sale-service/staffs/6/staff-children, method put
                . body:
                    {
                        [1,5]
                    }
                . Nếu set thành công thì sẽ tạo thành chu trình: 1 -> 6 -> 4 -> 2 -> 1 ....
            - Đầu ra mong muốn:
                . status code: 400
                . code: 'Không thể gán nhân viên cấp dưới vì tạo thành chu trình'
        """

        body = [1, 5]
        r = client.put(f"{settings.API_PREFIX}/staffs/6/staff-children", json=body)
        assert r.status_code == 400
        response = r.json()
        assert response['message'] == 'Không thể gán nhân viên cấp dưới vì tạo thành chu trình'

