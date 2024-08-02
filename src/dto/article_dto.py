import datetime
from typing import Optional
import uuid

from pydantic import Field

from abstracts import base_dto
from tools import consts


class ArticleDTO(base_dto.PydanticBase):
    """
    DTO, содержащий данные о статье пользователя
    """

    id: uuid.UUID = Field(description="Идентификатор статьи", default=uuid.uuid4())
    user_id: uuid.UUID = Field(description="Идентификатор пользователя")
    user_name: str = Field(description="Имя пользователя")
    creation_date: datetime.datetime | None = Field(
        description="Дата написания статьи", default=datetime.datetime.now()
    )
    topic_name: str = Field(description="Название темы статьи")
    topic_id: uuid.UUID = Field(description="Идентификатор темы статьи")
    text: str = Field(
        description="Текст статьи", max_length=consts.Articles.MAX_ARTICLE_LENGTH
    )
    views: int | None = Field(description="Количество просмотров", default=0)


class ArticleCreateDTO(base_dto.PydanticBase):
    """
    DTO, содержащий данные для создания статьи
    """

    id: uuid.UUID = Field(description="Идентификатор статьи", default=uuid.uuid4())
    user_id: uuid.UUID = Field(description="Идентификатор пользователя")
    topic_id: uuid.UUID = Field(description="Идентификатор темы статьи")
    text: str = Field(
        description="Текст статьи", max_length=consts.Articles.MAX_ARTICLE_LENGTH
    )


class ArticleUpdateDTO(base_dto.PydanticBase):
    """
    DTO, содержащий данные для обновления статьи
    """

    id: uuid.UUID = Field(description="Идентификатор статьи", default=uuid.uuid4())
    user_id: uuid.UUID = Field(description="Идентификатор пользователя")
    topic_id: Optional[uuid.UUID] = Field(
        description="Идентификатор темы статьи", default=None
    )
    text: Optional[str] = Field(
        description="Текст статьи",
        max_length=consts.Articles.MAX_ARTICLE_LENGTH,
        default=None,
    )


class ArticleRetrieveDTO(base_dto.PydanticBase):
    """
    DTO, содержащий данные о полученной из БД статье
    """

    id: uuid.UUID = Field(description="Идентификатор статьи", default=uuid.uuid4())
    user_id: uuid.UUID = Field(description="Идентификатор пользователя")
    topic_id: uuid.UUID = Field(description="Идентификатор темы статьи")
    creation_date: datetime.datetime | None = Field(description="Дата написания статьи")
    text: str = Field(
        description="Текст статьи", max_length=consts.Articles.MAX_ARTICLE_LENGTH
    )
    views: int | None = Field(description="Количество просмотров")
