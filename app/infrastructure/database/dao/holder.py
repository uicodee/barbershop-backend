from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.dao.rdb import (
    BaseDAO,
    EmployeeDAO,
    ClientDAO,
    SuperuserDAO,
    BranchDAO,
    AppointmentDAO,
    MessageTemplateDAO,
)


class HolderDao:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.base = BaseDAO
        self.employee = EmployeeDAO(self.session)
        self.client = ClientDAO(self.session)
        self.superuser = SuperuserDAO(self.session)
        self.branch = BranchDAO(self.session)
        self.appointment = AppointmentDAO(self.session)
        self.message_template = MessageTemplateDAO(self.session)
