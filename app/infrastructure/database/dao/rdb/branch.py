from pydantic import TypeAdapter
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app import dto
from app.api import schems
from app.infrastructure.database.dao.rdb import BaseDAO
from app.infrastructure.database.models import Branch


class BranchDAO(BaseDAO[Branch]):
    def __init__(self, session: AsyncSession):
        super().__init__(Branch, session)

    async def create(self, branch: schems.Branch) -> dto.Branch:
        branch = Branch(**branch.dict())
        self.session.add(branch)
        await self.session.commit()
        return dto.Branch.from_orm(branch)

    async def get_all(self) -> list[dto.Branch]:
        result = await self.session.execute(select(Branch))
        adapter = TypeAdapter(list[dto.Branch])
        return adapter.validate_python(result.scalars().all())

    async def get_by_name(
        self,
        name: str,
    ) -> dto.Branch:
        result = await self.session.execute(select(Branch).where(Branch.name == name))
        branch = result.scalar()
        if branch is not None:
            return dto.Branch.from_orm(branch)

    async def get_branch(
        self,
        branch_id: int,
    ) -> dto.Branch:
        result = await self.session.execute(
            select(Branch).where(Branch.id == branch_id)
        )
        branch = result.scalar()
        if branch is not None:
            return dto.Branch.from_orm(branch)

    async def update_branch(self, branch_id: int, branch: schems.Branch) -> dto.Branch:
        result = await self.session.execute(
            update(Branch)
            .where(Branch.id == branch_id)
            .values(**branch.dict())
            .returning(Branch)
        )
        await self.session.commit()
        return dto.Branch.model_validate(result.scalar())

    async def delete_branch(self, branch_id: int):
        await self.session.execute(delete(Branch).where(Branch.id == branch_id))
        await self.session.commit()
