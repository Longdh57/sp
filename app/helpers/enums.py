import enum


class StaffStatus(int, enum.Enum):
    ACTIVE = 1
    DISABLE = -1
