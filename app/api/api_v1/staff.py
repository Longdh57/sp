import logging
from fastapi import Depends
from typing import Any, List

from fastapi import APIRouter
from fastapi_sqlalchemy import db
from sqlalchemy import desc, asc
from sqlalchemy.orm import aliased

from app.models.staff import Staff
from app.schema.staff import StaffResponse, StaffRequest
from app.schema.base import ResponseSchemaBase
from app.helpers.enums import StaffStatus
from app.utils.paging import PaginationParams, paginate, Page

router = APIRouter()

logger = logging.getLogger()


@router.get("/", response_model=Page[StaffResponse])
def get_staffs(params: PaginationParams = Depends()) -> Any:
    try:
        result = paginate(db.session.query(Staff), params)
        return result
    except Exception as e:
        logger.info("error happen")
        logger.error(e)


@router.get("/{staff_id}", response_model=StaffResponse)
def get_staff(staff_id: int):
    try:
        return db.session.query(Staff).filter_by(id=staff_id).first()
    except Exception as e:
        logger.info(e)


@router.post("/", response_model=StaffResponse)
def create_staff(staff: StaffRequest):
    try:
        staff_db = Staff(
            staff_code=staff.staff_code,
            full_name=staff.full_name,
            email=staff.email,
            mobile=staff.mobile,
            is_superuser=staff.is_superuser,
            status=StaffStatus.ACTIVE
        )
        db.session.add(staff_db)
        db.session.commit()
        return staff_db
    except Exception as e:
        logger.info(e)


@router.put("/{staff_id}", response_model=StaffResponse)
def update_staff(staff_id: int, staff: StaffRequest):
    try:
        staff_db = db.session.query(Staff).filter_by(id=staff_id).first()
        if not staff_db:
            return None

        staff_db.staff_code = staff.staff_code
        staff_db.full_name = staff.full_name
        staff_db.email = staff.email
        staff_db.mobile = staff.mobile
        staff_db.is_superuser = staff.is_superuser

        db.session.commit()
        return staff_db
    except Exception as e:
        logger.info(e)


@router.put("/set-parent/{staff_id}", response_model=ResponseSchemaBase)
def update_staff_parent(staff_id: int, parent_id: int):
    try:
        staff_db = db.session.query(Staff).filter_by(id=staff_id).first()
        if not staff_db:
            return None

        parent_db = db.session.query(Staff).filter_by(id=parent_id).first()
        if not parent_db:
            return None

        staff_db.parent = parent_db
        db.session.commit()
        return ResponseSchemaBase().success_response()
    except Exception as e:
        logger.info(e)


@router.get("/get-staff-child/{staff_id}", response_model=List[StaffResponse])
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

        # staffs = db.session.query(Staff).filter(Staff.id.in_(staff_ids)).order_by(desc(Staff.id)).all()
        staffs = db.session.query(Staff).filter(Staff.id.in_(staff_ids)).order_by(asc(Staff.id)).all()

        return staffs
    except Exception as e:
        logger.info(e)
