import datetime
import uuid

import sqlalchemy as sa
from sqlalchemy import orm

from abstracts import abstract_alchemy_model


class User(abstract_alchemy_model.Base):
    """
    Модель Алхимии для пользователя
    """

    __tablename__ = "user"

    id = sa.Column(
        sa.UUID,
        primary_key=True,
        comment="Идентификатор пользователя",
        default=lambda: str(uuid.uuid4()),
    )
    name = sa.Column(sa.String, comment="Имя пользователя")
    hashed_password = sa.Column(sa.String, comment="Хешированный пароль")
    registration_date = sa.Column(
        sa.DateTime, comment="Дата регистрации", default=datetime.datetime.now()
    )
    articles = orm.relationship("Article", back_populates="user")
