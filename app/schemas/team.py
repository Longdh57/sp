from pydantic import BaseModel
from typing import Optional


class TeamResponse(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None
    type: int
    description: Optional[str] = None

    class Config:
        orm_mode = True


class TeamRequest(BaseModel):
    name: str
    code: str
    type: int
    description: Optional[str] = None
