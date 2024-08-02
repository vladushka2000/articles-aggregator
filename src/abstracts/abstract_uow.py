from __future__ import annotations  # no qa

import abc

from abstracts import abstract_repository


class AbstractUOW(abc.ABC):
    """
    Абстрактный класс UOW
    """

    def __init__(self) -> None:
        """
        Инициализировать переменные
        """

        self.repositories: dict[str, abstract_repository.AbstractRepository] = {}

    def add_repository(
        self, repository_name: str, repository: abstract_repository.AbstractRepository
    ) -> None:
        """
        Добавить репозиторий
        :param repository_name: название репозитория
        :param repository: объект репозитория
        """

        self.repositories[repository_name] = repository

    async def __aenter__(self, *args, **kwargs) -> AbstractUOW:
        """
        Войти в асинхронный контекстный менеджер
        """

        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        """
        Выйти из асинхронного контекстного менеджера
        """

        await self.rollback()

    @abc.abstractmethod
    async def commit(self) -> None:
        """
        Сделать коммит изменений
        """

        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self) -> None:
        """
        Сделать откат изменений
        """

        raise NotImplementedError


class AbstractUOWComposite(AbstractUOW):
    """
    Абстрактный компоновщик для UOW
    """

    def __init__(self) -> None:
        """
        Инициализировать переменные
        """

        self.uows: dict[str, AbstractUOW] = {}

        super().__init__()

    def add_uow(self, uow_name: str, uow: AbstractUOW) -> None:
        """
        Добавить объект UOW
        :param uow_name: название UOW
        :param uow: объект UOW
        """

        self.uows[uow_name] = uow

    async def commit(self) -> None:
        """
        Сделать коммит изменений
        """

        for uow in self.uows.values():
            await uow.commit()

    async def rollback(self) -> None:
        """
        Сделать откат изменений
        """

        for uow in self.uows.values():
            await uow.rollback()
