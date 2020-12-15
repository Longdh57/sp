from app.models.base_model import BareBaseModel

from sqlalchemy import Column, Integer, ForeignKey
from app.helpers.enums import TeamRole


class StaffTeam(BareBaseModel):
    staff_id = Column(Integer, ForeignKey('staff.id'), index=True, unique=True)
    team_id = Column(Integer, ForeignKey('team.id'))
    role = Column(Integer, default=TeamRole.MEMBER.value)
