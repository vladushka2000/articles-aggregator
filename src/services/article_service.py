import datetime
import uuid

from dependency_injector.wiring import Provide
from pydantic import Field
from redis.asyncio.client import Pipeline
from sqlalchemy.ext.asyncio import AsyncSession

from abstracts import abstract_repository, abstract_service, abstract_uow, base_dto
from dto import article_dto, user_dto
from tools import consts, di_container, enums


class ArticleService(abstract_service.AbstractService):
    """
    Сервис для работы с логикой авторизации и аутентификации
    """

    class __DIFactoriesObjectsDTO(base_dto.PydanticBase):
        """
        DTO для объектов, получаемых из фабрик DI-контейнеров
        """

        alchemy_session: AsyncSession = Field(description="Сессия Алхимии")
        redis_session: Pipeline = Field(description="Сессия Redis")

        article_alchemy_repository: abstract_repository.AbstractAlchemyRepository = (
            Field(description="Репозиторий для работы со статьями в связке с Алхимией")
        )
        article_redis_repository: abstract_repository.AbstractRedisRepository = Field(
            description="Репозиторий для работы со статьями в связке с Redis"
        )
        topic_repository: abstract_repository.AbstractAlchemyRepository = Field(
            description="Репозиторий для работы с темами статей"
        )

        alchemy_uow: abstract_uow.AbstractUOW = Field(
            description="UOW для работы с репозиториями Алхимии"
        )
        redis_uow: abstract_uow.AbstractUOW = Field(
            description="UOW для работы с репозиториями Redis"
        )
        alchemy_redis_uow_composite: abstract_uow.AbstractUOWComposite = Field(
            description="Компоновщик UOW для работы с репозиториями Алхимии и Redis"
        )

    alchemy_session_factory = Provide[
        di_container.SessionContainer.alchemy_session_factory
    ]
    redis_article_session_factory = Provide[
        di_container.SessionContainer.redis_article_session_factory
    ]

    article_alchemy_repository_factory = Provide[
        di_container.RepositoryContainer.article_alchemy_repository_factory
    ]
    article_redis_repository_factory = Provide[
        di_container.RepositoryContainer.article_redis_repository_factory
    ]
    topic_repository_factory = Provide[
        di_container.RepositoryContainer.topic_repository_factory
    ]

    alchemy_uow_factory = Provide[di_container.UOWContainer.alchemy_uow_factory]
    redis_uow_factory = Provide[di_container.UOWContainer.redis_uow_factory]
    alchemy_redis_uow_composite_factory = Provide[
        di_container.UOWContainer.alchemy_redis_uow_composite_factory
    ]

    @classmethod
    async def __get_di_objects(cls) -> __DIFactoriesObjectsDTO:
        """
        Получить объекты из фабрик DI-контейнеров
        """

        async with cls.alchemy_session_factory.session_maker() as async_session:
            alchemy_session = async_session

        redis_session = cls.redis_article_session_factory()

        article_alchemy_repository = cls.article_alchemy_repository_factory(
            alchemy_session
        )
        article_redis_repository = cls.article_redis_repository_factory(redis_session)
        topic_repository = cls.topic_repository_factory(alchemy_session)

        alchemy_uow = cls.alchemy_uow_factory()
        alchemy_uow.add_repository(
            article_alchemy_repository.name, article_alchemy_repository
        )
        alchemy_uow.add_repository(topic_repository.name, topic_repository)

        redis_uow = cls.redis_uow_factory()
        redis_uow.add_repository(
            article_redis_repository.name, article_redis_repository
        )

        alchemy_redis_uow_composite = cls.alchemy_redis_uow_composite_factory()
        alchemy_redis_uow_composite.add_uow(
            enums.UOWName.ALCHEMY_UOW.value, alchemy_uow
        )
        alchemy_redis_uow_composite.add_uow(enums.UOWName.REDIS_UOW.value, redis_uow)

        return cls.__DIFactoriesObjectsDTO(
            alchemy_session=alchemy_session,
            redis_session=redis_session,
            article_alchemy_repository=article_alchemy_repository,
            article_redis_repository=article_redis_repository,
            topic_repository=topic_repository,
            alchemy_uow=alchemy_uow,
            redis_uow=redis_uow,
            alchemy_redis_uow_composite=alchemy_redis_uow_composite,
        )

    @classmethod
    async def create_article(
        cls,
        user_model: user_dto.UserInfoDTO,
        article_model: article_dto.ArticleCreateDTO,
    ) -> article_dto.ArticleDTO:
        """
        Выполнить логику создания статьи
        :param user_model: объект информации о пользователе
        :param article_model: объект статьи
        :return: созданная статья
        """

        di_objects = await cls.__get_di_objects()

        async with di_objects.alchemy_uow:
            topic = await di_objects.alchemy_uow.repositories[
                di_objects.topic_repository.name
            ].retrieve(article_model.topic_id)
            article = article_dto.ArticleDTO(
                id=article_model.id,
                user_id=user_model.id,
                user_name=user_model.name,
                topic_id=topic.id,
                topic_name=topic.name,
                creation_date=datetime.datetime.now(),
                text=article_model.text,
                views=0,
            )
            di_objects.alchemy_uow.repositories[
                di_objects.article_alchemy_repository.name
            ].create(article)

            await di_objects.alchemy_uow.commit()

        return article

    @classmethod
    async def retrieve_article(cls, article_id: uuid.UUID) -> article_dto.ArticleDTO:
        """
        Выполнить логику создания статьи
        :param article_id: идентификатор статьи
        :return: полученная статья
        """

        di_objects = await cls.__get_di_objects()
        uow = di_objects.alchemy_uow

        async with uow:
            article_db = await uow.repositories[
                di_objects.article_alchemy_repository.name
            ].retrieve(article_id)

            article = article_dto.ArticleDTO(
                id=article_db.id,
                user_id=article_db.user_id,
                user_name=article_db.user_name,
                topic_id=article_db.topic_id,
                topic_name=article_db.topic_name,
                creation_date=article_db.creation_date,
                text=article_db.text,
                views=article_db.views + 1,
            )

            await di_objects.alchemy_uow.repositories[
                di_objects.article_alchemy_repository.name
            ].update(article)

            await di_objects.alchemy_uow.commit()

        return article

    @classmethod
    async def update_article(
        cls,
        user_model: user_dto.UserInfoDTO,
        article_model: article_dto.ArticleUpdateDTO,
    ) -> article_dto.ArticleDTO:
        """
        Выполнить логику обновления статьи
        :param user_model: объект информации о пользователе
        :param article_model: объект статьи
        :return: обновленная статья
        """

        di_objects = await cls.__get_di_objects()

        uow = di_objects.alchemy_redis_uow_composite

        async with uow:
            article_db = (
                await uow.uows[enums.UOWName.ALCHEMY_UOW.value]
                .repositories[enums.RepositoryName.ARTICLE_ALCHEMY_REPOSITORY.value]
                .retrieve(str(article_model.id))
            )

            if article_db is None:
                raise ValueError("Статья не была найдена в базе данных")

            if article_db.user_id != user_model.id:
                raise ValueError("Пользователь не является автором статьи")

            topic = None

            if article_model.topic_id is not None:
                topic = (
                    await uow.uows[enums.UOWName.ALCHEMY_UOW.value]
                    .repositories[enums.RepositoryName.TOPIC_REPOSITORY.value]
                    .retrieve(str(article_model.topic_id))
                )

                if topic is None:
                    raise ValueError("Тема статьи не была найдена в базе данных")

            article = article_dto.ArticleDTO(
                id=article_db.id,
                user_id=user_model.id,
                user_name=user_model.name,
                creation_date=article_db.creation_date,
                topic_name=topic.name if topic is not None else article_db.topic_name,
                topic_id=topic.id if topic is not None else article_db.topic_id,
                text=(
                    article_model.text
                    if article_model.text is not None
                    else article_db.text
                ),
                views=article_db.views,
            )

            await uow.uows[enums.UOWName.ALCHEMY_UOW.value].repositories[
                enums.RepositoryName.ARTICLE_ALCHEMY_REPOSITORY.value
            ].update(article)

            article_redis_repo_keys = list(article.model_fields.keys())

            (
                uow.uows[enums.UOWName.REDIS_UOW.value]
                .repositories[enums.RepositoryName.ARTICLE_REDIS_REPOSITORY.value]
                .retrieve(str(article.id), article_redis_repo_keys)
            )

            redis_article = await uow.uows[enums.UOWName.REDIS_UOW.value].commit()

            if not redis_article:
                await uow.uows[enums.UOWName.REDIS_UOW.value].repositories[
                    enums.RepositoryName.ARTICLE_REDIS_REPOSITORY.value
                ].create(article)

            await uow.commit()

        return article

    @classmethod
    async def delete_article(
        cls, user_model: user_dto.UserInfoDTO, article_id: uuid.UUID
    ) -> None:
        """
        Выполнить логику удаления статьи
        :param user_model: объект информации о пользователе
        :param article_id: идентификатор статьи
        :return: количество удаленных записей
        """

        di_objects = await cls.__get_di_objects()

        uow = di_objects.alchemy_redis_uow_composite

        async with uow:
            article_db = (
                await uow.uows[enums.UOWName.ALCHEMY_UOW.value]
                .repositories[enums.RepositoryName.ARTICLE_ALCHEMY_REPOSITORY.value]
                .retrieve(str(article_id))
            )

            if article_db is None:
                raise ValueError("Статья не была найдена в базе данных")

            if article_db.user_id != user_model.id:
                raise ValueError("Пользователь не является автором статьи")

            await uow.uows[enums.UOWName.ALCHEMY_UOW.value].repositories[
                enums.RepositoryName.ARTICLE_ALCHEMY_REPOSITORY.value
            ].delete(str(article_id))

            uow.uows[enums.UOWName.REDIS_UOW.value].repositories[
                enums.RepositoryName.ARTICLE_REDIS_REPOSITORY.value
            ].delete(str(article_id))

            await uow.commit()

    @classmethod
    async def update_popular_articles(
        cls, date_from: datetime.datetime, articles_num: int
    ) -> None:
        """
        Выполнить логику обновления списка лучших статей
        :param date_from: дата обновления статей
        :param articles_num: количество статей для обновления
        """

        di_objects = await cls.__get_di_objects()

        uow = di_objects.alchemy_redis_uow_composite

        async with uow:
            articles = (
                await uow.uows[enums.UOWName.ALCHEMY_UOW.value]
                .repositories[enums.RepositoryName.ARTICLE_ALCHEMY_REPOSITORY.value]
                .retrieve_by_date(date_from, articles_num)
            )

            if not articles:
                print("За рассматриваемый период не было опубликовано новых статей")

                return

            await uow.uows[enums.UOWName.REDIS_UOW.value].repositories[
                enums.RepositoryName.ARTICLE_REDIS_REPOSITORY.value
            ].retrieve_keys()

            current_redis_keys = (
                await uow.uows[enums.UOWName.REDIS_UOW.value].commit()
            )[0]

            if current_redis_keys:
                await uow.uows[enums.UOWName.REDIS_UOW.value].repositories[
                    enums.RepositoryName.ARTICLE_REDIS_REPOSITORY.value
                ].delete(*current_redis_keys)

            for article in articles:
                await uow.uows[enums.UOWName.REDIS_UOW.value].repositories[
                    enums.RepositoryName.ARTICLE_REDIS_REPOSITORY.value
                ].create(article)

            await uow.commit()

    @classmethod
    async def retrieve_popular_articles(cls) -> list[article_dto.ArticleDTO]:
        """
        Выполнить логику получения списка лучших статей
        :return: список популярных статей
        """

        di_objects = await cls.__get_di_objects()

        uow = di_objects.redis_uow

        async with uow:
            await uow.repositories[
                enums.RepositoryName.ARTICLE_REDIS_REPOSITORY.value
            ].retrieve_keys()

            article_ids = (await uow.commit())[0]

            if not article_ids:
                print("За рассматриваемый период не было опубликовано новых статей")

                return []

            result = []
            article_redis_repo_keys = list(article_dto.ArticleDTO.model_fields.keys())

            for article_id in article_ids:
                await uow.repositories[
                    enums.RepositoryName.ARTICLE_REDIS_REPOSITORY.value
                ].retrieve(article_id, article_redis_repo_keys)

                article_model_fields = (await uow.commit())[0]
                article_model_fields = [
                    field.decode("utf-8") for field in article_model_fields
                ]

                result.append(
                    article_dto.ArticleDTO(
                        id=uuid.UUID(article_model_fields[0]),
                        user_id=uuid.UUID(article_model_fields[1]),
                        user_name=article_model_fields[2],
                        creation_date=datetime.datetime.strptime(
                            article_model_fields[3],
                            consts.Articles.DATETIME_STRING_FORMAT,
                        ),
                        topic_name=article_model_fields[4],
                        topic_id=uuid.UUID(article_model_fields[5]),
                        text=article_model_fields[6],
                        views=article_model_fields[7],
                    )
                )

            return result
