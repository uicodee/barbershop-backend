from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.models import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .branch import Branch


class MessageTemplate(BaseModel):
    __tablename__ = "message_template"

    branch_id: Mapped[int] = mapped_column(ForeignKey("branch.id", ondelete="CASCADE"))
    text: Mapped[str] = mapped_column(Text)

    branch: Mapped["Branch"] = relationship(back_populates="message_templates")
