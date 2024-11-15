from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.models import BaseModel


class MessageTemplate(BaseModel):

    __tablename__ = "message_template"

    branch_id: Mapped[int] = mapped_column(ForeignKey("branch.id", ondelete="CASCADE"))
    text: Mapped[str] = mapped_column(Text)
