from app.models.base_model import BareBaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.helpers.enums import StaffStatus


class Staff(BareBaseModel):
    full_name = Column(String(200))
    staff_code = Column(String(200), nullable=True)
    email = Column(String(200), unique=True, index=True)
    mobile = Column(String(200))
    status = Column(Integer, default=StaffStatus.ACTIVE.value)
    alias = Column(String(200))
    is_superuser = Column(Boolean(), default=False)

    parent_id = Column(Integer, ForeignKey("staff.id"))
    parent = relationship("Staff", remote_side='Staff.id')
