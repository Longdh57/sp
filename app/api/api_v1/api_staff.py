import logging
from fastapi import Depends
from typing import Any, List

from fastapi import APIRouter
from fastapi_sqlalchemy import db
from sqlalchemy import asc
from sqlalchemy.orm import aliased

from app.models.staff import Staff
from app.schemas.staff import StaffResponse, StaffRequest
from app.schemas.base import ResponseSchemaBase
from app.utils.paging import PaginationParams, paginate, Page

router = APIRouter()

logger = logging.getLogger()


@router.get("/", response_model=Page[StaffResponse])
def get_staffs(params: PaginationParams = Depends()) -> Any:
    try:
        result = paginate(db.session.query(Staff), params)
        return result
    except Exception as e:
        logger.error(e)


@router.get("/{staff_id}", response_model=StaffResponse)
def get_staff(staff_id: int):
    try:
        return db.session.query(Staff).filter_by(id=staff_id).first()
    except Exception as e:
        logger.info(e)


@router.put("/{staff_id}", response_model=StaffResponse)
def update_staff(staff_id: int, staff: StaffRequest):
    try:
        staff_db = db.session.query(Staff).filter_by(id=staff_id).first()
        if not staff_db:
            return ResponseSchemaBase().fail_response(404, "Không tìm thấy nhân viên!")

        staff_db.status = staff.status
        staff_db.alias = staff.alias

        db.session.commit()
        return staff_db
    except Exception as e:
        logger.info(e)


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


@router.put("/{staff_id}/set-staff-child", response_model=ResponseSchemaBase)
def update_staff_parent(staff_child_ids: List[int], staff_id: int):
    try:
        staff_db = db.session.query(Staff).filter_by(id=staff_id).first()
        if not staff_db:
            return ResponseSchemaBase().fail_response(404, "Không tìm thấy nhân viên!")

        if not staff_child_ids:
            return ResponseSchemaBase().fail_response(400, "Danh sách nhân viên cấp dưới không được rỗng!")

        childs_db = db.session.query(Staff).filter(Staff.id.in_(staff_child_ids))
        if childs_db.count() != len(staff_child_ids):
            return ResponseSchemaBase().fail_response(404, "Không tìm thấy 1 hoặc nhiều nhân viên cấp dưới!")

        childs_db.update(
            {Staff.parent_id: staff_id},
            synchronize_session=False
        )
        db.session.commit()
        return ResponseSchemaBase().success_response()
    except Exception as e:
        logger.info(e)
        return ResponseSchemaBase().fail_response(500, "Có lỗi xảy ra!")


@router.get("/{staff_id}/get-staff-child", response_model=List[StaffResponse])
def get_staff_child(staff_id: int):
    try:
        staff_db = db.session.query(Staff).filter_by(id=staff_id).first()
        if not staff_db:
            return None

        included = db.session.query(Staff.id).filter(Staff.parent_id == staff_id).cte(name="included", recursive=True)

        included_alias = aliased(included, name="parent")
        staff_alias = aliased(Staff, name="child")

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

        return staffs
    except Exception as e:
        logger.info(e)

