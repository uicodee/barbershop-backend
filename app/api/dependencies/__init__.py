from apscheduler_di import ContextSchedulerDecorator
from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker

from app.api.dependencies.authentication import (
    AuthProvider,
    get_employee,
    get_superuser,
)
from app.api.dependencies.database import DbProvider, dao_provider
from app.api.dependencies.scheduler import get_scheduler
from app.api.dependencies.settings import get_settings
from app.config import Settings, load_config


def setup(
    app: FastAPI,
    pool: sessionmaker,
    settings: Settings,
    scheduler: ContextSchedulerDecorator,
):
    db_provider = DbProvider(pool=pool)
    auth_provider = AuthProvider(settings=settings)
    app.dependency_overrides[get_employee] = auth_provider.get_current_employee
    app.dependency_overrides[get_superuser] = auth_provider.get_current_superuser
    app.dependency_overrides[dao_provider] = db_provider.dao
    app.dependency_overrides[AuthProvider] = lambda: auth_provider
    app.dependency_overrides[get_scheduler] = lambda: scheduler
    app.dependency_overrides[get_settings] = load_config
