import enum


class Role(str, enum.Enum):
    ADMIN = 'admin'
    BACKOFFICE = 'backoffice'
