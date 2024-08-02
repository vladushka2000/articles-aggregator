import datetime
import uuid

import strawberry


@strawberry.type
class UserModelBase:
    """
    Базовая модель данных о пользователе
    """

    id: uuid.UUID
    name: str


@strawberry.type
class UserModel(UserModelBase):
    """
    Модель данных о пользователе
    """

    id: uuid.UUID
    name: str
    registration_date: datetime.datetime
