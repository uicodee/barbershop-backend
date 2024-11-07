from datetime import datetime

from pydantic import Field

from app.dto import BaseModelWithDateTime
from .types import ReminderStatus


class Reminder(BaseModelWithDateTime):

    sent_at: datetime = Field(alias="sentAt")
    status: ReminderStatus = Field()
