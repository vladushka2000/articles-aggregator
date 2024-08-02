from redis.asyncio.client import Pipeline
from sqlalchemy.ext.asyncio import AsyncSession

from abstracts import abstract_factory
from tools import enums
from repositories import (
    article_repository,
    token_repository,
    topic_repository,
    user_repository,
)


class UserRepositoryFactory(abstract_factory.AbstractFactory):
    """
    Фабрика репозиториев для работы с пользователями
    """

    def __call__(self, session: AsyncSession) -> user_repository.UserRepository:
        """
        Создать объект репозитория
        :param session: сессия Алхимии
        """

        return user_repository.UserRepository(
            enums.RepositoryName.USER_REPOSITORY.value, session
        )


class ArticleAlchemyRepositoryFactory(abstract_factory.AbstractFactory):
    """
    Фабрика репозиториев для работы со статьями в связке с Алхимией
    """

    def __call__(
        self, session: AsyncSession
    ) -> article_repository.ArticleAlchemyRepository:
        """
        Создать объект репозитория
        :param session: сессия Алхимии
        """

        return article_repository.ArticleAlchemyRepository(
            enums.RepositoryName.ARTICLE_ALCHEMY_REPOSITORY.value, session
        )


class TopicAlchemyRepositoryFactory(abstract_factory.AbstractFactory):
    """
    Фабрика репозиториев для работы с темами статей в связке с Алхимией
    """

    def __call__(self, session: AsyncSession) -> topic_repository.TopicRepository:
        """
        Создать объект репозитория
        :param session: сессия Алхимии
        """

        return topic_repository.TopicRepository(
            enums.RepositoryName.TOPIC_REPOSITORY.value, session
        )


class ArticleRedisRepositoryFactory(abstract_factory.AbstractFactory):
    """
    Фабрика репозиториев для работы со статьями в связке с Redis
    """

    def __call__(self, session: Pipeline) -> article_repository.ArticleRedisRepository:
        """
        Создать объект репозитория
        :param session: сессия Redis
        """

        return article_repository.ArticleRedisRepository(
            enums.RepositoryName.ARTICLE_REDIS_REPOSITORY.value, session
        )


class TokenRepositoryFactory(abstract_factory.AbstractFactory):
    """
    Фабрика репозиториев для работы с репозиторием токенов
    """

    def __call__(self, session: Pipeline) -> token_repository.TokenRepository:
        """
        Создать объект репозитория
        :param session: сессия Redis
        """

        return token_repository.TokenRepository(
            enums.RepositoryName.TOKEN_REPOSITORY.value, session
        )
