from pydantic import BaseModel
from typing import Optional


class StaffResponse(BaseModel):
    id: Optional[int] = None
    staff_code: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    status: int
    alias: Optional[str] = None

    class Config:
        orm_mode = True


class StaffRequest(BaseModel):
    status: int
    alias: str
