from app.models.base_model import BareBaseModel

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from app.helpers.enums import TeamType


class Team(BareBaseModel):
    name = Column(String(50))
    code = Column(String(20), unique=True, index=True)
    type = Column(Integer, default=TeamType.TEAM_SALE.value)
    description = Column(String(200))

    members = relationship("Staff", secondary="staffteam")
