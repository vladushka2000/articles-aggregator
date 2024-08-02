import contextlib

from apscheduler.schedulers import asyncio
from fastapi import FastAPI
import uvicorn

from scheduler import scheduler_jobs
from tools import app_config, consts, di_container
from web.tools import router_registrator

config = app_config.config


@contextlib.asynccontextmanager
async def lifespan(fast_api_app: FastAPI) -> None:  # no qa
    """
    Подготовить ресурсы для FastAPI-приложения
    :param fast_api_app: приложение FastAPI
    """

    scheduler = asyncio.AsyncIOScheduler()
    scheduler.add_job(
        scheduler_jobs.update_popular_articles,
        trigger="interval",
        seconds=consts.Articles.MOST_VIEWED_ARTICLE_LIFETIME_IN_SEC,
        args=[
            consts.Articles.MOST_VIEWED_ARTICLE_LIFETIME_IN_SEC,
            consts.Articles.POPULAR_ARTICLES_COUNT,
        ],
    )

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

    yield

    scheduler.shutdown()


app = FastAPI(
    debug=config.is_dev,
    title=config.app_name,
    version=config.app_version,
    lifespan=lifespan,
)
router_registrator.register_routers(app, config.app_mode)


if __name__ == "__main__":
    session_container = di_container.SessionContainer()
    repository_container = di_container.RepositoryContainer()
    uow_container = di_container.UOWContainer()

    modules = [
        "services.article_service",
        "services.auth_service",
        "services.user_service",
    ]

    session_container.wire(modules=modules)
    repository_container.wire(modules=modules)
    uow_container.wire(modules=modules)

    print(f"Приложение запущено в режиме {config.app_mode.value}")

    uvicorn.run(app, host=config.app_host, port=config.app_port)
