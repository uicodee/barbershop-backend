from pydantic import BaseModel, Field


class Employee(BaseModel):
    full_name: str = Field(
        title="Fullname",
        description="User Fullname"
    )
    branch_id: int = Field(
        title="Branch",
        description="Branch ID"
    )


class LoginEmployee(BaseModel):
    email: str = Field(
        title="Email",
        description="User email",
        min_length=5
    )
    password: str = Field(
        title="Password",
        description="Employee password"
    )


class RegisterEmployee(Employee):
    email: str = Field(
        title="Email",
        description="Employee email",
        min_length=5
    )
    password: str = Field(
        title="Password",
        description="Employee password",
        min_length=6
    )
