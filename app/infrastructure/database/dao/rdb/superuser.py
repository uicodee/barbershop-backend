from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import dto
from app.infrastructure.database.dao.rdb import BaseDAO
from app.infrastructure.database.models import Superuser


class SuperuserDAO(BaseDAO[Superuser]):
    def __init__(self, session: AsyncSession):
        super().__init__(Superuser, session)

    async def create(
            self,
            full_name: str,
            username: str,
            password: str
    ) -> dto.Superuser:
        superuser = Superuser(
            full_name=full_name,
            username=username,
            password=password
        )
        self.session.add(superuser)
        await self.session.commit()
        return dto.Superuser.from_orm(superuser)

    async def get_superuser(
            self,
            username: str,
            with_password: bool = False
    ) -> dto.Superuser | dto.SuperuserWithPassword:
        result = await self.session.execute(
            select(Superuser).where(Superuser.username == username)
        )
        superuser = result.scalar()
        if superuser is not None:
            if with_password:
                return dto.SuperuserWithPassword.from_orm(superuser)
            else:
                return dto.Superuser.from_orm(superuser)
