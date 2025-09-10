from enum import StrEnum


class SquareStatus(StrEnum):
    CLOSED = 'closed'
    AVAILABLE = 'available'
    OPENED = 'opened'
    CLEARED = 'cleared'
