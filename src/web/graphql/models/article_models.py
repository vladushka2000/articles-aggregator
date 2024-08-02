import datetime
from typing import Optional
import uuid

import strawberry

from web.graphql.models import user_models


@strawberry.type
class TopicType:
    """
    Тип данных для темы статьи
    """

    id: uuid.UUID
    name: str


@strawberry.type
class ArticleType:
    """
    Тип данных для статьи
    """

    id: uuid.UUID
    user: user_models.UserModelBase
    creation_date: datetime.datetime = strawberry.field()
    topic: TopicType
    text: str
    views: int


@strawberry.input
class ArticleCreateInput:
    """
    Тип данных для создания статьи
    """

    topic_id: uuid.UUID
    text: str


@strawberry.input
class ArticleUpdateInput:
    """
    Тип данных для обновления статьи
    """

    id: uuid.UUID
    topic_id: Optional[uuid.UUID] = None
    text: Optional[str] = None
