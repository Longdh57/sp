from pydantic import BaseModel
from typing import Optional


class StaffResponse(BaseModel):
    id: Optional[int] = None
    staff_code: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    status: int
    is_superuser: Optional[bool] = False

    class Config:
        orm_mode = True


class StaffRequest(BaseModel):
    staff_code: str
    full_name: str
    email: str
    mobile: str
    is_superuser: bool = False
