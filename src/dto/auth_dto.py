import uuid

from pydantic import Field

from abstracts import base_dto


class AuthDTO(base_dto.PydanticBase):
    """
    DTO, содержащий данные о регистрации пользователя
    """

    name: str = Field(description="Имя пользователя")
    password: str = Field(description="Пароль")
