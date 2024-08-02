from pydantic import field_validator

from tools import validators


class UserNameCheckMixin:
    """
    Миксин для проверки имени пользователя требованиям
    """

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str) -> str:
        """
        Провалидировать имя пользователя
        :param name: имя
        :return: имя пользователя, в случае удачной валидации
        """

        return validators.validate_name(name)
