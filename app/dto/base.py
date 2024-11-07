from datetime import datetime

import pytz
from pydantic import BaseModel as PydanticBaseModel, Field


def serialize_time(value: datetime) -> int:
    return int(value.timestamp())


class Base(PydanticBaseModel):
    class Config:
        from_attributes = True
        populate_by_name = True
        json_encoders = {
            datetime: serialize_time
        }


class BaseModel(Base):
    id: int


class BaseModelWithDateTime(BaseModel):
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
