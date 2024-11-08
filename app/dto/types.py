from enum import Enum


class AppointmentStatus(str, Enum):
    SCHEDULED = "SCHEDULED"
    ARRIVED = "ARRIVED"
    ARRIVED_EARLY = "ARRIVED_EARLY"
    MISSED = "MISSED"


class ReminderStatus(str, Enum):

    SENT = "SENT"
    FAILED = "FAILED"
