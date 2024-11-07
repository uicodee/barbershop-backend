import uvicorn as uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler_di import ContextSchedulerDecorator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import sessionmaker

from app.api import controllers, dependencies
from app.config import load_config
from app.domain.data import job_stores
from app.infrastructure.database.factory import create_pool, make_connection_string


def main() -> FastAPI:
    settings = load_config()
    scheduler = ContextSchedulerDecorator(AsyncIOScheduler(jobstores=job_stores))
    app = FastAPI(
        title="Barbershop",
        docs_url="/docs",
        version="1.0.0"
    )
    pool = create_pool(url=make_connection_string(settings=settings))
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    dependencies.setup(
        app=app,
        pool=pool,
        settings=settings,
        scheduler=scheduler
    )
    # scheduler.ctx.add_instance(bot, Bot)
    # scheduler.ctx.add_instance(translator_hub, TranslatorHub)
    scheduler.ctx.add_instance(pool, sessionmaker)
    scheduler.start()
    controllers.setup(app)
    return app


if __name__ == '__main__':
    uvicorn.run(
        "app.api.__main__:main",
        host="0.0.0.0",
        port=15400,
        reload=True
    )
