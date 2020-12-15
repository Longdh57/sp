import enum


class StaffStatus(int, enum.Enum):
    ACTIVE = 1
    DISABLE = -1


class TeamType(int, enum.Enum):
    TEAM_SALE = 0
    TEAM_CHAIN = 1
    TEAM_SCC = 2
