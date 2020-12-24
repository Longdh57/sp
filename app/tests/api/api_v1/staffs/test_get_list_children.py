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

    def test_get_staff_tree(self, client: TestClient):
        """
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
            - Gọi API get toàn bộ nhân viên theo cây phân quyền
                . API: ../sale-service/staffs/staff-tree
            - Đầu ra mong muốn:
                . status code: 200
                . code: '000'
                . list data không null, không empty, size = 2 ( vì hiện tại có 2 cha là user 1 và user 7)
                    . Nhân viên cha đầu tiên có id = 1, email = binh.dh@teko.vn
                    . Nhân viên cha thứ 2 có id = 7, email = g.teko@teko.vn
                . Trong nhân viên cha thứ nhất có 2 node:
                    . node1 là user có id= 2, email = a.teko@teko.vn
                        . Trong node1 này có 1 node(node1.1) là user4 có email = c.teko@teko.vn
                            . Trong node1.1 này có 1 lá(node1.1.1) là user6 có email = e.teko@teko.vn
                    . node2 là user có id= 3, email = b.teko@teko.vn
                        . Trong node2 này có 1 lá(node2.1) là user5 có email = d.teko@teko.vn
                . Trong nhân viên cha thứ hai có 1 node:
                    . node1 là user có id= 8, email = h.teko@teko.vn, trong node1 này list children empty ( đây là lá)
        """
        r = client.get(f"{settings.API_PREFIX}/staffs/staff-tree")
        assert r.status_code == 200
        response = r.json()
        assert response['code'] == '000'
        assert response['data'] is not None and len(response['data']) == 2
        assert response['data'][0]['id'] == 1 and response['data'][0]['email'] == 'binh.dh@teko.vn'
        assert response['data'][1]['id'] == 7 and response['data'][1]['email'] == 'g.teko@teko.vn'

        # Test with first parent node
        assert response['data'][0]['children'] is not None and len(response['data'][0]['children']) == 2
        node1 = response['data'][0]['children'][0]
        node2 = response['data'][0]['children'][1]
        assert node1['id'] == 2 and node1['email'] == 'a.teko@teko.vn'
        assert node2['id'] == 3 and node2['email'] == 'b.teko@teko.vn'

        assert node1['children'] is not None and len(node1['children']) == 1
        assert node2['children'] is not None and len(node2['children']) == 1

        node11 = node1['children'][0]
        node21 = node2['children'][0]

        assert node11['email'] == 'c.teko@teko.vn'
        assert node21['email'] == 'd.teko@teko.vn'

        assert node11['children'] is not None and len(node11['children']) == 1
        node111 = node11['children'][0]
        assert node111['email'] == 'e.teko@teko.vn'
        assert node111['children'] is not None and len(node111['children']) == 0

        assert node21['children'] is not None and len(node21['children']) == 0

        # Test with second parent node
        assert response['data'][1]['children'] is not None and len(response['data'][1]['children']) == 1
        node1 = response['data'][1]['children'][0]
        assert node1['id'] == 8 and node1['email'] == 'h.teko@teko.vn'
        assert node1['children'] is not None and len(node1['children']) == 0

    def test_get_staff_not_found(self, client: TestClient):
        """
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
            - Gọi API get cây phân quyền của user có id=9 ( không tồn tại user này trong hệ thống)
                . API: ../sale-service/staffs/9/staff-children-tree
            - Đầu ra mong muốn:
                . status code: 404
                . message: 'Không tìm thấy nhân viên'
        """
        r = client.get(f"{settings.API_PREFIX}/staffs/9/staff-children-tree")
        assert r.status_code == 404
        response = r.json()
        assert response['message'] == 'Không tìm thấy nhân viên'

    def test_get_node(self, client: TestClient):
        """
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
            - Gọi API get cây phân quyền của user có id=2
                . API: ../sale-service/staffs/2/staff-children-tree
            - Đầu ra mong muốn:
                . status code: 200
                . code: '000'
                . data không null, không empty:
                    . data có: id = 2, email = a.teko@teko.vn
                . user2 có 1 node(node1) là user4: id = 4, email = c.teko@teko.vn
                    . Trong node1 này có 1 node(node1.1) là user6 có id = 6, email = e.teko@teko.vn
        """
        r = client.get(f"{settings.API_PREFIX}/staffs/2/staff-children-tree")
        assert r.status_code == 200
        staffs = r.json()
        assert staffs['code'] == '000'
        assert staffs['data'] is not None and staffs['data'] != {}
        assert staffs['data']['id'] == 2 and staffs['data']['email'] == 'a.teko@teko.vn'

        assert staffs['data']['children'] is not None and len(staffs['data']['children']) == 1
        node1 = staffs['data']['children'][0]
        assert node1['id'] == 4 and node1['email'] == 'c.teko@teko.vn'
        assert node1['children'] is not None and len(node1['children']) == 1

        node11 = node1['children'][0]
        assert node11['id'] == 6 and node11['email'] == 'e.teko@teko.vn'
        assert node11['children'] is not None and len(node11['children']) == 0

    def test_get_node_leaf(self, client: TestClient):
        """
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
            - Gọi API get cây phân quyền của user có id=8 (node lá trong cây phân quyền)
                . API: ../sale-service/staffs/8/staff-children-tree
            - Đầu ra mong muốn:
                . status code: 200
                . code: '000'
                . data không null, không empty:
                    . data có: id = 8, email = h.teko@teko.vn
                . user8 là note lá nên list children empty: children = []
        """
        r = client.get(f"{settings.API_PREFIX}/staffs/8/staff-children-tree")
        assert r.status_code == 200
        response = r.json()
        assert response['code'] == '000'
        assert response['data'] is not None and response['data'] != {}
        assert response['data']['id'] == 8 and response['data']['email'] == 'h.teko@teko.vn'

        assert response['data']['children'] is not None and len(response['data']['children']) == 0


