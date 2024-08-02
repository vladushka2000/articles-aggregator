from dependency_injector import containers, providers

from tools.factories import session_factory
from tools.factories import repository_factory, uow_factory


class SessionContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами сессий
    """

    alchemy_session_factory = providers.Factory(session_factory.AlchemySessionFactory)
    redis_article_session_factory = providers.Factory(
        session_factory.RedisArticleSessionFactory
    )
    redis_token_session_factory = providers.Factory(
        session_factory.RedisTokenSessionFactory
    )


class RepositoryContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами репозиториев
    """

    article_alchemy_repository_factory = providers.Factory(
        repository_factory.ArticleAlchemyRepositoryFactory
    )
    article_redis_repository_factory = providers.Factory(
        repository_factory.ArticleRedisRepositoryFactory
    )
    user_repository_factory = providers.Factory(
        repository_factory.UserRepositoryFactory
    )
    topic_repository_factory = providers.Factory(
        repository_factory.TopicAlchemyRepositoryFactory
    )
    token_repository_factory = providers.Factory(
        repository_factory.TokenRepositoryFactory
    )


class UOWContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами UOW
    """

    alchemy_uow_factory = providers.Factory(uow_factory.AlchemyUOWFactory)
    redis_uow_factory = providers.Factory(uow_factory.RedisUOWFactory)
    alchemy_redis_uow_composite_factory = providers.Factory(
        uow_factory.AlchemyRedisUOWCompositeFactory
    )
