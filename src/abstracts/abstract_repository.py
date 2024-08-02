import abc

import redis.asyncio as redis
from sqlalchemy.ext import asyncio as alchemy_asyncio


class AbstractRepository(abc.ABC):
    """
    Абстрактный класс репозитория
    """

    def __init__(self, name: str) -> None:
        """
        Инициализировать переменные
        :param name: название репозитория
        """

        self.name = name


class CreateMixin:
    """
    Миксин репозитория, содержащего метод create
    """

    @abc.abstractmethod
    def create(self, *args, **kwargs) -> any:
        """
        Создать записи
        """

        raise NotImplementedError


class RetrieveMixin:
    """
    Миксин репозитория, содержащего метод retrieve
    """

    @abc.abstractmethod
    def retrieve(self, *args, **kwargs) -> any:
        """
        Получить записи
        """

        raise NotImplementedError


class UpdateMixin:
    """
    Миксин репозитория, содержащего метод update
    """

    @abc.abstractmethod
    def update(self, *args, **kwargs) -> any:
        """
        Обновить записи
        """

        raise NotImplementedError


class DeleteMixin:
    """
    Миксин репозитория, содержащего метод delete
    """

    @abc.abstractmethod
    def delete(self, *args, **kwargs) -> any:
        """
        Удалить записи
        """

        raise NotImplementedError


class AbstractAlchemyRepository(AbstractRepository):
    """
    Абстрактный класс репозитория Алхимии
    """

    def __init__(self, name: str, session: alchemy_asyncio.AsyncSession) -> None:
        """
        Инициализировать переменные
        :param name: название репозитория
        :param session: сессия Алхимии
        """

        super().__init__(name)

        self.session = session


class AbstractRedisRepository(AbstractRepository):
    """
    Абстрактный класс репозитория Redis
    """

    def __init__(self, name: str, session: redis.client.Pipeline) -> None:
        """
        Инициализировать переменные
        :param name: название репозитория
        :param session: сессия Redis
        """

        super().__init__(name)

        self.session = session
