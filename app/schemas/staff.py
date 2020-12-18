from pydantic import BaseModel
from typing import Optional, List


class StaffResponse(BaseModel):
    id: Optional[int] = None
    staff_code: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    status: int = 1
    alias: Optional[str] = None

    class Config:
        orm_mode = True


class StaffTreeResponse(StaffResponse):
    parent_id: Optional[int] = None
    children: Optional[List] = []


class StaffRequest(BaseModel):
    status: int
    alias: str
