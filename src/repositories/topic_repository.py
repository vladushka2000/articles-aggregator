import uuid

from sqlalchemy import select

from abstracts import abstract_repository as abs_repo
from dto import topic_dto
from repositories.models import article_model


class TopicRepository(abs_repo.AbstractAlchemyRepository, abs_repo.RetrieveMixin):
    """
    Репозиторий для работы с темами статей
    """

    async def retrieve(self, topic_id: uuid.UUID) -> topic_dto.TopicDTO | None:
        """
        Получить запись темы статьи
        :param topic_id: идентификатор статьи
        """

        query = select(article_model.ArticleTopic).where(
            article_model.ArticleTopic.id == topic_id
        )
        result = await self.session.execute(query)
        result = result.scalars().first()

        if result is None:
            return

        return topic_dto.TopicDTO(id=result.id, name=result.name)
