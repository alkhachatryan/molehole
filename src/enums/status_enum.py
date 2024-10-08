from enum import Enum

class StatusEnum(str, Enum):
    SUCCESSFUL_CONNECTION = 'SUCCESSFUL_CONNECTION'
    AUTH_FAILED = 'AUTH_FAILED'