import asyncio

from app.api.dependencies import AuthProvider
from app.config import load_config
from app.infrastructure.database.dao import HolderDao
from app.infrastructure.database.factory import make_connection_string, create_pool


class Creator:
    def __init__(self):
        self.settings = load_config()
        self.auth_provider = AuthProvider(settings=self.settings)
        self.pool = create_pool(url=make_connection_string(settings=self.settings))

    async def create_superuser(self):
        full_name = input(">> Enter fullname: ")
        username = input(">> Enter username: ")
        password = input(">> Enter password: ")
        async with self.pool() as session:
            dao = HolderDao(session=session)
            if await dao.superuser.get_superuser(username=username) is None:
                await dao.superuser.create(
                    full_name=full_name,
                    username=username,
                    password=self.auth_provider.get_password_hash(password=password),
                )

    async def create_all(self):
        await self.create_superuser()


creator = Creator()
asyncio.run(creator.create_all())
