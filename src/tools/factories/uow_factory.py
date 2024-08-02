from abstracts import abstract_factory
from uow import alchemy_uow, alchemy_redis_uow_composite, redis_uow


class AlchemyUOWFactory(abstract_factory.AbstractFactory):
    """
    Фабрика UOW для работы с репозиториями Алхимии
    """

    def __call__(self) -> alchemy_uow.AlchemyUOW:
        """
        Создать объект UOW
        """

        return alchemy_uow.AlchemyUOW()


class RedisUOWFactory(abstract_factory.AbstractFactory):
    """
    Фабрика UOW для работы с репозиториями Redis
    """

    def __call__(self) -> redis_uow.RedisUOW:
        """
        Создать объект UOW
        """

        return redis_uow.RedisUOW()


class AlchemyRedisUOWCompositeFactory(abstract_factory.AbstractFactory):
    """
    Фабрика компоновщика UOW для работы с репозиториями Алхимии и Redis
    """

    def __call__(self) -> alchemy_redis_uow_composite.AlchemyRedisUOWComposite:
        """
        Создать объект компоновщика UOW
        """

        return alchemy_redis_uow_composite.AlchemyRedisUOWComposite()
