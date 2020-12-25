import logging
from fastapi import Depends
from typing import Any, List

from fastapi import APIRouter
from fastapi_sqlalchemy import db
from sqlalchemy import asc
from sqlalchemy.orm import aliased

from app.helpers.exception_type import ExceptionType
from app.models.staff import Staff
from app.schemas.staff import StaffResponse, StaffRequest, StaffTreeResponse
from app.schemas.base import ResponseSchemaBase, DataResponse
from app.utils.exception_handler import SaleServiceException
from app.utils.paging import PaginationParams, paginate, Page
from pydantic import parse_obj_as

router = APIRouter()

logger = logging.getLogger()


@router.get("/", response_model=Page[StaffResponse])
def get_staffs(params: PaginationParams = Depends(), email: str = None, phone: str = None, status: int = None) -> Any:
    query = db.session.query(Staff)
    if email:
        query = query.filter(Staff.email.like("%{}%".format(email)))
    if phone:
        query = query.filter(Staff.mobile.like("%{}%".format(phone)))
    if status or status == 0:
        if status != -1 and status != 1:
            raise SaleServiceException(ExceptionType.STAFF_STATUS_INVALID)
        else:
            query = query.filter(Staff.status == status)
    return paginate(query, params)


@router.get("/staff-tree", response_model=DataResponse[List[StaffTreeResponse]])
def get_staff_tree():
    staffs = db.session.query(Staff).order_by(asc(Staff.id)).all()
    return format_staff_tree(staffs, None)


@router.get("/{staff_id}", response_model=DataResponse[StaffResponse])
def get_staff(staff_id: int):
    result = db.session.query(Staff).filter_by(id=staff_id).first()
    if not result:
        raise SaleServiceException(ExceptionType.SALE_NOT_FOUND)
    else:
        return DataResponse().success_response(result)


# @router.post("/", response_model=StaffResponse)
# def create_staff(staff: StaffRequest):
#     try:
#         staff_db = Staff(
#             staff_code=staff.staff_code,
#             full_name=staff.full_name,
#             email=staff.email,
#             mobile=staff.mobile,
#             is_superuser=staff.is_superuser,
#             status=StaffStatus.ACTIVE
#         )
#         db.session.add(staff_db)
#         db.session.commit()
#         return staff_db
#     except Exception as e:
#         logger.info(e)


@router.put("/{staff_id}", response_model=ResponseSchemaBase)
def update_staff(staff_id: int, staff: StaffRequest):
    staff_db = db.session.query(Staff).filter_by(id=staff_id).first()
    if not staff_db:
        raise SaleServiceException(ExceptionType.SALE_NOT_FOUND)

    if not staff.status or (staff.status != -1 and staff.status != 1):
        raise SaleServiceException(ExceptionType.STAFF_STATUS_INVALID)

    staff_db.status = staff.status
    staff_db.alias = staff.alias

    db.session.commit()
    return ResponseSchemaBase().success_response()


@router.put("/{staff_id}/parent/{parent_id}", response_model=ResponseSchemaBase)
def update_staff_parent(staff_id: int, parent_id: int):
    staff_db = db.session.query(Staff).filter_by(id=staff_id).first()
    if not staff_db:
        raise SaleServiceException(ExceptionType.SALE_NOT_FOUND)

    parent_db = db.session.query(Staff).filter_by(id=parent_id).first()
    if not parent_db:
        raise SaleServiceException(http_code=400, code='400', message='Không tìm thấy nhân viên cấp trên')

    staff_children_id = get_staff_children_id([staff_id])
    if parent_id in staff_children_id:
        raise SaleServiceException(http_code=400, code='400',
                                   message='Không thể gán nhân viên cấp trên vì tạo thành chu trình')

    staff_db.parent = parent_db
    db.session.commit()
    return ResponseSchemaBase().success_response()


@router.put("/{staff_id}/staff-children", response_model=ResponseSchemaBase)
def update_staff_children(staff_children_id: List[int], staff_id: int):
    staff_db = db.session.query(Staff).filter_by(id=staff_id).first()
    if not staff_db:
        raise SaleServiceException(ExceptionType.SALE_NOT_FOUND)

    if not staff_children_id:
        raise SaleServiceException(http_code=400, code='400',
                                   message='Danh sách nhân viên cấp dưới không được rỗng')

    children_db = db.session.query(Staff).filter(Staff.id.in_(staff_children_id))
    if children_db.count() != len(staff_children_id):
        raise SaleServiceException(http_code=400, code='400',
                                   message='Không tìm thấy 1 hoặc nhiều nhân viên cấp dưới')

    staff_children_id_check = get_staff_children_id(staff_children_id)

    if staff_id in staff_children_id_check:
        raise SaleServiceException(http_code=400, code='400',
                                   message='Không thể gán nhân viên cấp dưới vì tạo thành chu trình')

    children_db.update(
        {Staff.parent_id: staff_id},
        synchronize_session=False
    )
    db.session.commit()
    return ResponseSchemaBase().success_response()


@router.get("/{staff_id}/staff-children", response_model=DataResponse[List[StaffResponse]])
def get_staff_children(staff_id: int):
    staff_db = db.session.query(Staff).filter_by(id=staff_id).first()
    if not staff_db:
        raise SaleServiceException(ExceptionType.SALE_NOT_FOUND)

    staff_ids = get_staff_children_id([staff_id])

    staffs = db.session.query(Staff).filter(Staff.id.in_(staff_ids)).order_by(asc(Staff.id)).all()

    return DataResponse().success_response(staffs)


@router.get("/{staff_id}/staff-children-tree", response_model=DataResponse[StaffTreeResponse])
def get_tree_staff_children(staff_id: int):
    staff_db = db.session.query(Staff).filter_by(id=staff_id).first()
    if not staff_db:
        raise SaleServiceException(ExceptionType.SALE_NOT_FOUND)

    staff_ids = get_staff_children_id([staff_id])

    staffs = db.session.query(Staff).filter(Staff.id.in_(staff_ids)).order_by(asc(Staff.parent_id), asc(Staff.id)).all()

    return format_staff_tree(staffs, staff_id)


def get_staff_children_id(staff_ids: List[int]):
    included = db.session.query(Staff.id).filter(Staff.parent_id.in_(staff_ids)).cte(name="included", recursive=True)

    included_alias = aliased(included, name="parent")
    staff_alias = aliased(Staff, name="children")

    included = included.union_all(
        db.session.query(
            staff_alias.id
        ).filter(
            staff_alias.parent_id == included_alias.c.id
        )
    )

    staff_ids = map(
        lambda _tuple: _tuple[0],
        [(staff_id, ) for staff_id in staff_ids] + db.session.query(included.c.id).distinct().all(),
    )

    return staff_ids


def format_staff_tree(staff_dbs: List[Staff], root_id: int):
    map_staff = {}
    staffs = []
    root = []
    i = 0

    # init map staff
    for staff in staff_dbs:
        staffs.append(parse_obj_as(StaffTreeResponse, staff))
        map_staff[staff.id] = i
        i += 1

    for staff in staffs:
        # Get staff tree of 1 staff
        if root_id is not None:
            if staff.id != root_id:
                staffs[map_staff[staff.parent_id]].children.append(staff)
            else:
                root = staff
        # Get staff tree of all staff
        else:
            if staff.parent_id is not None:
                staffs[map_staff[staff.parent_id]].children.append(staff)
            else:
                root.append(staff)

    return DataResponse().success_response(root)
