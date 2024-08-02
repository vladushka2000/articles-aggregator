from pydantic import Field

from abstracts import base_dto
from web.fast_api.models.mixins import username_check_mixin, password_check_mixin


class AuthModel(
    base_dto.BaseModel,
    password_check_mixin.PasswordCheckMixin,
    username_check_mixin.UserNameCheckMixin,
):
    """
    Модель для регистрации и входа пользователя в систему
    """

    name: str = Field(description="Имя пользователя")
    password: str = Field(description="Пароль")
