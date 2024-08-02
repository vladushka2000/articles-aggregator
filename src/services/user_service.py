import uuid

from dependency_injector.wiring import Provide
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession

from abstracts import abstract_repository, abstract_service, abstract_uow, base_dto
from tools import di_container
from dto import user_dto


class UserService(abstract_service.AbstractService):
    """
    Сервис для работы с логикой действия над пользователями
    """

    class __DIFactoriesObjectsDTO(base_dto.PydanticBase):
        """
        DTO для объектов, получаемых из фабрик DI-контейнеров
        """

        alchemy_session: AsyncSession = Field(description="Сессия Алхимии")

        user_repository: abstract_repository.AbstractAlchemyRepository = Field(
            description="Репозиторий для работы с пользователями"
        )

        alchemy_uow: abstract_uow.AbstractUOW = Field(
            description="UOW для работы с репозиториями Алхимии"
        )

    alchemy_session_factory = Provide[
        di_container.SessionContainer.alchemy_session_factory
    ]

    user_repository_factory = Provide[
        di_container.RepositoryContainer.user_repository_factory
    ]

    alchemy_uow_factory = Provide[di_container.UOWContainer.alchemy_uow_factory]

    @classmethod
    async def __get_di_objects(cls) -> __DIFactoriesObjectsDTO:
        """
        Получить объекты из фабрик DI-контейнеров
        """

        async with cls.alchemy_session_factory.session_maker() as async_session:
            alchemy_session = async_session

        user_repository = cls.user_repository_factory(alchemy_session)

        alchemy_uow = cls.alchemy_uow_factory()
        alchemy_uow.add_repository(user_repository.name, user_repository)

        return cls.__DIFactoriesObjectsDTO(
            alchemy_session=alchemy_session,
            user_repository=user_repository,
            alchemy_uow=alchemy_uow,
        )

    @classmethod
    async def get_user(cls, user_id: uuid.UUID) -> user_dto.UserDTO:
        """
        Выполнить логику получения данных пользователя
        :param user_id: идентификатор пользователя
        :return: токены
        """

        di_objects = await cls.__get_di_objects()

        async with di_objects.alchemy_uow:
            user = await di_objects.alchemy_uow.repositories[
                di_objects.user_repository.name
            ].retrieve(user_id=str(user_id))

            if user is None:
                raise ValueError("Пользователь не найден")

        return user_dto.UserDTO(
            id=user.id,
            name=user.name,
            password=user.password,
            registration_date=user.registration_date,
        )
