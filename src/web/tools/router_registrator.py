from fastapi import FastAPI

from tools import enums
from web.fast_api.entrypoints import (
    article_entrypoint as article_entrypoint_rest,
    auth_entrypoint as auth_entrypoint_rest,
    user_entrypoint as user_entrypoint_rest,
)
from web.graphql.entrypoints import (
    article_entrypoint as article_entrypoint_graph,
    auth_entrypoint as auth_entrypoint_graph,
    user_entrypoint as user_entrypoint_graph,
)


def register_routers(app: FastAPI, app_mode: enums.AppWorkingMode) -> None:
    """
    Зарегистрировать роутеры
    :param app: приложение FastAPI
    :param app_mode: режим работы приложения
    """

    match app_mode:
        case enums.AppWorkingMode.REST:
            app.include_router(article_entrypoint_rest.router)
            app.include_router(auth_entrypoint_rest.router)
            app.include_router(user_entrypoint_rest.router)
        case enums.AppWorkingMode.GRAPHQL:
            app.include_router(article_entrypoint_graph.router)
            app.include_router(auth_entrypoint_graph.router)
            app.include_router(user_entrypoint_graph.router)
        case _:
            raise ValueError("Неизвестный тип режима работы приложения")
