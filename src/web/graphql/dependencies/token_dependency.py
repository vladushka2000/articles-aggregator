from strawberry.fastapi import BaseContext

from tools import consts
from web.tools import token_validator


class TokenDependency(BaseContext):
    """
    Класс зависимости для получения токена
    """

    def __get_token(self) -> str | None:
        """
        Получить токен из запроса
        :return: токен
        """

        if not self.request:
            return

        return self.request.headers["Authorization"]

    def get_access_token(self) -> str | None:
        """
        Получить access-токен
        :return: access-токен
        """

        token = self.__get_token()

        return (
            token_validator.validate_token(token, consts.Auth.ACCESS_TOKEN_ATTRS)
            if token
            else None
        )

    def get_refresh_token(self) -> str | None:
        """
        Получить refresh-токен
        :return: refresh-токен
        """

        token = self.__get_token()

        return (
            token_validator.validate_token(token, consts.Auth.REFRESH_TOKEN_ATTRS)
            if token
            else None
        )


async def get_token() -> TokenDependency:
    """
    Получить зависимость для токенов
    :return: зависимость для токенов
    """

    return TokenDependency()
