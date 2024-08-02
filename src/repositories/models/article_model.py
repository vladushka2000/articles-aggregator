import uuid

import sqlalchemy as sa
from sqlalchemy import orm

from tools import consts
from abstracts import abstract_alchemy_model


class ArticleTopic(abstract_alchemy_model.Base):
    """
    Модель Алхимии для темы статьи
    """

    __tablename__ = "article_topic"

    id = sa.Column(
        sa.UUID,
        primary_key=True,
        comment="Идентификатор темы статьи",
        default=lambda: str(uuid.uuid4()),
    )
    name = sa.Column(sa.String, comment="Название темы статьи")
    article_ids = orm.relationship("Article", back_populates="topic")


class Article(abstract_alchemy_model.Base):
    """
    Модель Алхимии для статьи
    """

    __tablename__ = "article"

    id = sa.Column(
        sa.UUID,
        primary_key=True,
        comment="Идентификатор статьи",
        default=lambda: str(uuid.uuid4()),
    )
    user_id = sa.Column(
        sa.UUID, sa.ForeignKey("user.id"), comment="Идентификатор пользователя"
    )
    user = orm.relationship("User", back_populates="articles")
    creation_date = sa.Column(sa.DateTime, comment="Дата создания статьи")
    topic_id = sa.Column(
        sa.UUID, sa.ForeignKey("article_topic.id"), comment="Идентификатор темы статьи"
    )
    topic = orm.relationship("ArticleTopic", back_populates="article_ids")
    text = sa.Column(
        sa.String(length=consts.Articles.MAX_ARTICLE_LENGTH), comment="Текст статьи"
    )
    views = sa.Column(sa.Integer, comment="Количество просмотров")
