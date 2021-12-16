from enum import Enum

class databaseStatus(Enum):
    UPDATED = 1,
    STORED = 2,
    REMOVED = 3,
    ERROR = 4