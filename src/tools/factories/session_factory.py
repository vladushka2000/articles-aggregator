from typing import AsyncGenerator

from pydantic import RedisDsn
import redis.asyncio as redis
from sqlalchemy.ext import asyncio as alchemy_asyncio

from abstracts import abstract_factory
from tools import app_config


class AlchemySessionFactory(abstract_factory.AbstractFactory):
    """
    Фабрика сессий SQLAlchemy
    """

    def __init__(self) -> None:
        """
        Инициализировать переменные
        """
        dsn = str(app_config.config.postgres_dsn)
        echo = True if app_config.config.is_dev else False

        engine = alchemy_asyncio.create_async_engine(dsn, echo=echo)

        self.session_maker = alchemy_asyncio.async_sessionmaker(
            autocommit=False, bind=engine
        )

    async def __call__(self) -> AsyncGenerator[alchemy_asyncio.AsyncSession, None]:
        """
        Создать объект асинхронной сессии
        :return: объект асинхронной сессии
        """

        async with self.session_maker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


class BaseRedisSessionFactory(abstract_factory.AbstractFactory):
    """
    Базовая фабрика сессий Redis
    """

    def __init__(self, redis_dsn: RedisDsn) -> None:
        """
        Инициализировать переменные
        :param redis_dsn: Redis dsn
        """

        self.redis_session = redis.Redis(
            host=redis_dsn.host, port=redis_dsn.port
        ).pipeline()

    def __call__(self) -> redis.client.Pipeline:
        """
        Получить сессию Redis
        """

        return self.redis_session


class RedisTokenSessionFactory(BaseRedisSessionFactory):
    """
    Фабрика сессий Redis для работы с токенами
    """

    def __init__(self) -> None:
        """
        Инициализировать переменные
        """

        redis_dsn = app_config.config.redis_token_dsn
        super().__init__(redis_dsn)


class RedisArticleSessionFactory(BaseRedisSessionFactory):
    """
    Фабрика сессий Redis для работы со статьями
    """

    def __init__(self) -> None:
        """
        Инициализировать переменные
        """

        redis_dsn = app_config.config.redis_article_dsn
        super().__init__(redis_dsn)
