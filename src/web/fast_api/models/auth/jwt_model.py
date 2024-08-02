from pydantic import Field

from abstracts import base_dto


class JWTModel(base_dto.BaseModel):
    """
    Модель данных JWT-токенов
    """

    access_token: str = Field(description="Access-токен")
    refresh_token: str = Field(description="Refresh-токен")
