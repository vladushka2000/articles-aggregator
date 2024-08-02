import datetime
import uuid

from pydantic import Field

from abstracts import base_dto


class UserInfoDTO(base_dto.PydanticBase):
    """
    DTO, содержащий основную информацию о пользователе
    """

    id: uuid.UUID = Field(
        description="Идентификатор пользователя", default=uuid.uuid4()
    )
    name: str = Field(description="Имя пользователя")


class UserDTO(UserInfoDTO):
    """
    DTO, содержащий все данные о пользователе
    """

    password: str = Field(description="Пароль")
    registration_date: datetime.datetime = Field(description="Дата регистрации")
