import datetime
import uuid

from pydantic import Field

from abstracts import base_dto


class UserModel(base_dto.BaseModel):
    """
    Модель данных о пользователе
    """

    id: uuid.UUID = Field(description="Идентификатор пользователя")
    name: str = Field(description="Имя пользователя")
    registration_date: datetime.datetime = Field(description="Дата регистрации")
