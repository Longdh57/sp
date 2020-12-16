import logging
from fastapi import Depends
from typing import Any, List

from fastapi import APIRouter
from fastapi_sqlalchemy import db
from sqlalchemy import asc
from sqlalchemy.orm import aliased

from app.models.staff import Staff
from app.schemas.staff import StaffResponse, StaffRequest
from app.schemas.base import ResponseSchemaBase, DataResponse
from app.utils.paging import PaginationParams, paginate, Page
from pydantic import parse_obj_as

router = APIRouter()

logger = logging.getLogger()


@router.get("/", response_model=Page[StaffResponse])
def get_staffs(params: PaginationParams = Depends()) -> Any:
    try:
        result = paginate(db.session.query(Staff), params)
        return result
    except Exception as e:
        logger.error(e)


@router.get("/{staff_id}", response_model=DataResponse[StaffResponse])
def get_staff(staff_id: int):
    try:
        result = db.session.query(Staff).filter_by(id=staff_id).first()
        if not result:
            return DataResponse().fail_response(404, "Không tìm thấy nhân viên!")
        else:
            return DataResponse().success_response(result)
    except Exception as e:
        logger.info(e)
        return DataResponse().fail_response(500, "Có lỗi xảy ra!")


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
    try:
        staff_db = db.session.query(Staff).filter_by(id=staff_id).first()
        if not staff_db:
            return ResponseSchemaBase().fail_response(404, "Không tìm thấy nhân viên!")

        staff_db.status = staff.status
        staff_db.alias = staff.alias

        db.session.commit()
        return ResponseSchemaBase().success_response()
    except Exception as e:
        logger.info(e)
        return ResponseSchemaBase().fail_response(500, "Có lỗi xảy ra!")


@router.put("/{staff_id}/set-parent/{parent_id}", response_model=ResponseSchemaBase)
def update_staff_parent(staff_id: int, parent_id: int):
    try:
        staff_db = db.session.query(Staff).filter_by(id=staff_id).first()
        if not staff_db:
            return ResponseSchemaBase().fail_response(404, "Không tìm thấy nhân viên!")

        parent_db = db.session.query(Staff).filter_by(id=parent_id).first()
        if not parent_db:
            return ResponseSchemaBase().fail_response(404, "Không tìm thấy nhân viên cấp trên !")

        staff_db.parent = parent_db
        db.session.commit()
        return ResponseSchemaBase().success_response()
    except Exception as e:
        logger.info(e)
        return ResponseSchemaBase().fail_response(500, "Có lỗi xảy ra!")


@router.put("/{staff_id}/set-staff-children", response_model=ResponseSchemaBase)
def update_staff_parent(staff_children_id: List[int], staff_id: int):
    try:
        staff_db = db.session.query(Staff).filter_by(id=staff_id).first()
        if not staff_db:
            return ResponseSchemaBase().fail_response(404, "Không tìm thấy nhân viên!")

        if not staff_children_id:
            return ResponseSchemaBase().fail_response(400, "Danh sách nhân viên cấp dưới không được rỗng!")

        children_db = db.session.query(Staff).filter(Staff.id.in_(staff_children_id))
        if children_db.count() != len(staff_children_id):
            return ResponseSchemaBase().fail_response(404, "Không tìm thấy 1 hoặc nhiều nhân viên cấp dưới!")

        children_db.update(
            {Staff.parent_id: staff_id},
            synchronize_session=False
        )
        db.session.commit()
        return ResponseSchemaBase().success_response()
    except Exception as e:
        logger.info(e)
        return ResponseSchemaBase().fail_response(500, "Có lỗi xảy ra!")


@router.get("/{staff_id}/get-staff-children", response_model=DataResponse[List[StaffResponse]])
def get_staff_children(staff_id: int):
    try:
        staff_db = db.session.query(Staff).filter_by(id=staff_id).first()
        if not staff_db:
            return DataResponse().fail_response(404, 'Không tìm thấy nhân viên!')

        included = db.session.query(Staff.id).filter(Staff.parent_id == staff_id).cte(name="included", recursive=True)

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
            [(staff_id,)] + db.session.query(included.c.id).distinct().all(),
        )

        staffs = db.session.query(Staff).filter(Staff.id.in_(staff_ids)).order_by(asc(Staff.id)).all()

        return DataResponse().success_response(staffs)
    except Exception as e:
        logger.info(e)
        return DataResponse().fail_response(500, "Có lỗi xảy ra!")


@router.get("/{staff_id}/get-tree-staff-children")
def get_tree_staff_children(staff_id: int):
    try:
        staff_db = db.session.query(Staff).filter_by(id=staff_id).first()
        if not staff_db:
            return DataResponse().fail_response(404, 'Không tìm thấy nhân viên!')

        included = db.session.query(Staff.id).filter(Staff.parent_id == staff_id).cte(name="included", recursive=True)

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
            [(staff_id,)] + db.session.query(included.c.id).distinct().all(),
        )

        staffs = db.session.query(Staff).filter(Staff.id.in_(staff_ids)).order_by(asc(Staff.parent_id), asc(Staff.id)).all()

        return format_tree_staff(staffs, staff_id)
    except Exception as e:
        logger.info(e)
        return DataResponse().fail_response(500, "Có lỗi xảy ra!")


def format_tree_staff(staff_dbs: List[Staff], root_id: int):
    map_staff = {}
    staffs = []
    root = []
    i = 0

    # init map staff
    for staff in staff_dbs:
        staffs.append(parse_obj_as(StaffResponse, staff))
        staffs[i].parent_id = staff.parent_id
        staffs[i].children = []
        map_staff[staff.id] = i
        i += 1

    for staff in staffs:
        if staff.id != root_id:
            staffs[map_staff[staff.parent_id]].children.append(staff)
        else:
            root = staff

    return DataResponse().success_response(root)
