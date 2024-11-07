from pydantic import Field, BaseModel


class Branch(BaseModel):
    name: str = Field()
    location: str = Field()
