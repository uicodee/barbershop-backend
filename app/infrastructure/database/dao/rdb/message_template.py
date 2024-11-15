from pydantic import TypeAdapter
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app import dto
from app.api import schems
from app.infrastructure.database.dao.rdb import BaseDAO
from app.infrastructure.database.models import MessageTemplate


class MessageTemplateDAO(BaseDAO[MessageTemplate]):
    def __init__(self, session: AsyncSession):
        super().__init__(MessageTemplate, session)

    async def create(
        self, message_template: schems.MessageTemplate, branch_id: int
    ) -> dto.MessageTemplate:
        msg_template = MessageTemplate(text=message_template.text, branch_id=branch_id)
        self.session.add(msg_template)
        await self.session.commit()
        return dto.MessageTemplate.from_orm(msg_template)

    async def get_all(self) -> list[dto.MessageTemplate]:
        result = await self.session.execute(select(MessageTemplate))
        adapter = TypeAdapter(list[dto.MessageTemplate])
        return adapter.validate_python(result.scalars().all())

    async def get_all_by_branch(self, branch_id: int) -> list[dto.MessageTemplate]:
        result = await self.session.execute(
            select(MessageTemplate).where(MessageTemplate.branch_id == branch_id)
        )
        adapter = TypeAdapter(list[dto.MessageTemplate])
        return adapter.validate_python(result.scalars().all())

    async def get_one(
        self, message_template_id: int, branch_id: int
    ) -> dto.MessageTemplate:
        result = await self.session.execute(
            select(MessageTemplate).where(
                MessageTemplate.branch_id == branch_id,
                MessageTemplate.id == message_template_id,
            )
        )
        message_template = result.scalar()
        if message_template is not None:
            return dto.MessageTemplate.from_orm(message_template)

    async def update_message_template(
        self,
        branch_id: int,
        message_template: schems.MessageTemplate,
        message_template_id: int,
    ) -> dto.MessageTemplate:
        result = await self.session.execute(
            update(MessageTemplate)
            .where(
                MessageTemplate.branch_id == branch_id,
                MessageTemplate.id == message_template_id,
            )
            .values(text=message_template.text)
            .returning(MessageTemplate)
        )
        await self.session.commit()
        return dto.MessageTemplate.model_validate(result.scalar())

    async def delete_message_template(
        self, branch_id: int, message_template_id: int
    ) -> None:
        await self.session.execute(
            delete(MessageTemplate).where(
                MessageTemplate.branch_id == branch_id,
                MessageTemplate.id == message_template_id,
            )
        )
        await self.session.commit()
