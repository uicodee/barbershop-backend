from pydantic import Field

from app.dto import BaseModel
from .branch import Branch


class Employee(BaseModel):
    full_name: str = Field(alias="fullName")
    email: str

    branch: Branch = Field(default=None)


class EmployeeWithPassword(Employee):
    password: str
