from __future__ import annotations  # no qa

from sqlalchemy.ext.asyncio import AsyncSession

from abstracts import abstract_uow, abstract_repository


class AlchemyUOW(abstract_uow.AbstractUOW):
    """
    UOW для работы с репозиториями Алхимии
    """

    def __init__(self) -> None:
        """
        Инициализировать переменные
        """

        super().__init__()

        self.session: AsyncSession | None = None

    def add_repository(
        self,
        repository_name: str,
        repository: abstract_repository.AbstractAlchemyRepository,
    ) -> None:
        super().add_repository(repository_name, repository)

        if self.session is None:
            self.session = repository.session
        elif self.session is not repository.session:
            raise ValueError(
                "Взаимодействие с БД может происходить в рамках только одной сессии"
            )

    async def commit(self) -> None:
        """
        Сделать коммит изменений
        """

        await self.session.commit()

    async def rollback(self) -> None:
        """
        Сделать откат изменений
        """

        await self.session.rollback()
