import uuid

from pydantic import field_validator, Field

from abstracts import base_dto
from tools import enums


class TokenAttrsDTO(base_dto.PydanticBase):
    """
    DTO, содержащий данные о параметрах токена
    """

    token_type: enums.TokenType = Field(description="Тип токена")
    expiration_time_in_sec: int = Field(description="Время жизни токена в секундах")


class TokensDTO(base_dto.PydanticBase):
    """
    DTO, содержащий данные о токенах пользователя
    """

    access_token: str = Field(description="Access-токен")
    refresh_token: str = Field(description="Refresh-токен")


class UsersRefreshToken(base_dto.PydanticBase):
    """
    DTO, содержащий информацию о пользователе и его refresh_токене
    """

    user_id: str = Field(description="Идентификатор пользователя")
    refresh_token: str = Field(description="Refresh-токен")

    @field_validator("user_id", mode="before")
    @classmethod
    def convert_user_id_to_str(cls, user_id: uuid.UUID) -> str:
        """
        Конвертировать идентификатор пользователя из UUID в строку
        """

        return str(user_id)
