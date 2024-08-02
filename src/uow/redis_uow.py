from __future__ import annotations  # no qa

from redis.asyncio.client import Pipeline

from abstracts import abstract_uow, abstract_repository


class RedisUOW(abstract_uow.AbstractUOW):
    """
    UOW для работы с репозиториями Redis
    """

    def __init__(self) -> None:
        """
        Инициализировать переменные
        """

        super().__init__()

        self.session: Pipeline | None = None

    def add_repository(
        self,
        repository_name: str,
        repository: abstract_repository.AbstractRedisRepository,
    ) -> None:
        super().add_repository(repository_name, repository)

        if self.session is None:
            self.session = repository.session
        elif self.session is not repository.session:
            raise ValueError(
                "Взаимодействие с БД может происходить в рамках только одной сессии"
            )

    async def commit(self) -> list:
        """
        Сделать коммит изменений
        """

        return await self.session.execute()

    async def __aexit__(self, *args, **kwargs) -> None:
        """
        Выйти из асинхронного контекстного менеджера
        """

        pass

    async def rollback(self) -> None:
        """
        Сделать откат изменений
        """

        pass
