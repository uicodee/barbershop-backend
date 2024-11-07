from enum import Enum


class AppointmentStatus(str, Enum):
    SCHEDULED = "SCHEDULED"
    ARRIVED = "ARRIVED"
    MISSED = "MISSED"


class ReminderStatus(str, Enum):

    SENT = "SENT"
    FAILED = "FAILED"
