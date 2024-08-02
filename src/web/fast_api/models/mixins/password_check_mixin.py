from pydantic import field_validator

from tools import validators


class PasswordCheckMixin:
    """
    Миксин для проверки пароля требованиям
    """

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        """
        Провалидировать пароль
        :param password: пароль
        :return: пароль, в случае удачной валидации
        """

        return validators.validate_password(password)
