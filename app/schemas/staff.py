import pydantic
from pydantic import BaseModel
from typing import Optional


class StaffResponse(BaseModel):
    id: Optional[int] = None
    staff_code: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    status: int = 1
    alias: Optional[str] = None

    class Config:
        extra = pydantic.Extra.allow
        orm_mode = True


class StaffRequest(BaseModel):
    status: int = 1
    alias: str
