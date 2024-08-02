import datetime
from typing import Optional
import uuid

from pydantic import Field

from abstracts import base_dto
from tools import consts


class ArticleWriteModel(base_dto.BaseModel):
    """
    Модель данных для написания статьи
    """

    topic_id: uuid.UUID = Field(description="Идентификатор темы статьи")
    text: str = Field(
        description="Текст статьи", max_length=consts.Articles.MAX_ARTICLE_LENGTH
    )


class ArticleUpdateModel(base_dto.BaseModel):
    """
    Модель данных для обновления статьи
    """

    id: uuid.UUID = Field(description="Идентификатор статьи")
    topic_id: Optional[uuid.UUID] = Field(
        description="Идентификатор темы статьи", default=None
    )
    text: Optional[str] = Field(
        description="Текст статьи",
        max_length=consts.Articles.MAX_ARTICLE_LENGTH,
        default=None,
    )


class ArticleResultModel(base_dto.BaseModel):
    """
    Модель данных о существующей статье
    """

    id: uuid.UUID = Field(description="Идентификатор статьи")
    user_id: uuid.UUID = Field(description="Идентификатор автора статьи")
    user_name: str = Field(description="Имя автора статьи")
    creation_date: datetime.datetime = Field(description="Дата создания статьи")
    topic_id: uuid.UUID = Field(description="Идентификатор темы статьи")
    topic_name: str = Field(description="Название темы статьи")
    text: str = Field(
        description="Текст статьи", max_length=consts.Articles.MAX_ARTICLE_LENGTH
    )
    views: int = Field(description="Количество просмотров")
