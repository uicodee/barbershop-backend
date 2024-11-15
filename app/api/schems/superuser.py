from pydantic import BaseModel, Field


class LoginSuperuser(BaseModel):
    username: str = Field(title="Username", description="Superuser username")
    password: str = Field(title="Password", description="Employee password")
