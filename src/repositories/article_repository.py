import datetime

from sqlalchemy import delete, select, update
from sqlalchemy.orm import joinedload

from abstracts import abstract_repository as abs_repo
from dto import article_dto
from repositories.models import article_model
from tools import consts


class ArticleAlchemyRepository(
    abs_repo.AbstractAlchemyRepository,
    abs_repo.CreateMixin,
    abs_repo.RetrieveMixin,
    abs_repo.UpdateMixin,
    abs_repo.DeleteMixin,
):
    """
    Репозиторий для работы со статьями
    """

    def create(self, article: article_dto.ArticleDTO) -> None:
        """
        Создать запись статьи
        :param article: объект статьи
        """

        article_db_model = article_model.Article(
            id=article.id,
            user_id=article.user_id,
            creation_date=article.creation_date,
            topic_id=article.topic_id,
            text=article.text,
            views=article.views,
        )

        self.session.add(article_db_model)

    async def retrieve(self, article_id: str) -> article_dto.ArticleDTO | None:
        """
        Получить запись статьи
        :param article_id: идентификатор статьи
        """

        query = (
            select(article_model.Article)
            .options(
                joinedload(article_model.Article.topic),
                joinedload(article_model.Article.user),
            )
            .where(article_model.Article.id == article_id)
        )
        result = await self.session.execute(query)
        result = result.scalars().first()

        if result is None:
            return

        return article_dto.ArticleDTO(
            id=result.id,
            user_id=result.user_id,
            user_name=result.user.name,
            topic_id=result.topic_id,
            topic_name=result.topic.name,
            creation_date=result.creation_date,
            text=result.text,
            views=result.views,
        )

    async def retrieve_by_date(
        self, date_from: datetime.datetime, articles_count: int = None
    ) -> list[article_dto.ArticleDTO]:
        """
        Получить записи статей, опубликованных после date_from
        :param date_from: дата обновления статей
        :param articles_count: количество статей для получения
        :return: список статей, удовлетворяющих условиям
        """

        query = (
            select(article_model.Article)
            .options(
                joinedload(article_model.Article.topic),
                joinedload(article_model.Article.user),
            )
            .where(article_model.Article.creation_date >= date_from)
        )

        if articles_count is not None:
            query = query.limit(articles_count)

        result = await self.session.execute(query)
        result = result.scalars().all()

        if result is None:
            return

        return [
            article_dto.ArticleDTO(
                id=article.id,
                user_id=article.user_id,
                user_name=article.user.name,
                topic_id=article.topic_id,
                topic_name=article.topic.name,
                creation_date=article.creation_date,
                text=article.text,
                views=article.views,
            )
            for article in result
        ]

    async def update(self, article: article_dto.ArticleDTO) -> None:
        """
        Обновить статью
        :param article: объект статьи
        """

        query = (
            update(article_model.Article)
            .where(article_model.Article.id == article.id)
            .values(topic_id=article.topic_id, text=article.text, views=article.views)
        )

        await self.session.execute(query)

    async def delete(self, article_id: str) -> None:
        """
        Удалить запись статьи
        :param article_id: идентификатор статьи
        """

        query = delete(article_model.Article).where(
            article_model.Article.id == article_id
        )

        await self.session.execute(query)


class ArticleRedisRepository(
    abs_repo.AbstractRedisRepository,
    abs_repo.CreateMixin,
    abs_repo.RetrieveMixin,
    abs_repo.DeleteMixin,
):
    """
    Репозиторий для работы со статьями
    """

    async def create(self, article: article_dto.ArticleDTO) -> None:
        """
        Создать запись статьи
        :param article: объект данных о статье
        """

        article_db = dict(
            article_dto.ArticleDTO(
                id=article.id,
                user_id=article.user_id,
                user_name=article.user_name,
                creation_date=article.creation_date,
                topic_name=article.topic_name,
                topic_id=article.topic_id,
                text=article.text,
                views=article.views
            )
        )

        article_db["id"] = str(article_db["id"])
        article_db["user_id"] = str(article_db["user_id"])
        article_db["topic_id"] = str(article_db["topic_id"])
        article_db["creation_date"] = article_db["creation_date"].strftime(
            consts.Articles.DATETIME_STRING_FORMAT
        )

        await self.session.hset(name=article_db["id"], mapping=article_db)

    async def retrieve(self, article_id: str, keys: list[str]) -> list:
        """
        Получить статью
        :param article_id: идентификатор статьи
        :param keys: ключи, значения которых нужно получить
        :return: запись в БД в случае нахождения
        """

        return await self.session.hmget(article_id, keys)

    async def retrieve_keys(self) -> list:
        """
        Получить текущие ключи
        :return: список ключей
        """

        return await self.session.keys()

    async def delete(self, *article_ids: str) -> int:
        """
        Удалить статью
        :param article_ids: идентификаторы статей
        :return: количество удаленных статей
        """

        return await self.session.delete(*article_ids)
