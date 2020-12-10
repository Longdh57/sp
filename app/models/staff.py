from app.models.base_model import BareBaseModel
from sqlalchemy import Column, String, Integer

from app.helpers.enums import StaffStatus


class Staff(BareBaseModel):
    full_name = Column(String(200))
    staff_code = Column(String(200), nullable=True)
    email = Column(String(200), unique=True, index=True)
    mobile = Column(String(200))
    status = Column(Integer, default=StaffStatus.ACTIVE.value, index=True)