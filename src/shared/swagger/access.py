import enum


class Access(str, enum.Enum):
    PUBLIC = 'public'
    PROTECTED = 'protected'
    INTERNAL = 'internal'
