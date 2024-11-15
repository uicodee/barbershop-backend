from pydantic import BaseModel, Field


class MessageTemplate(BaseModel):
    text: str
    branch_id: int = Field(alias="branchId")


class DeleteMessageTemplate(BaseModel):
    branch_id: int = Field(alias="branchId")
    message_template_id: int = Field(alias="messageTemplateId")
