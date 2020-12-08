import enum


class StaffStatus(str, enum.Enum):
    ACTIVE = 1
    DISABLE = -1
