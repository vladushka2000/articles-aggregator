from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from tools import consts
from web.tools import token_validator

__http_bearer = HTTPBearer()


def get_access_token(
    creds: HTTPAuthorizationCredentials = Depends(__http_bearer),
) -> str:
    """
    Получить access-токен
    :param creds: данные авторизации
    :return: access-токен
    """

    return token_validator.validate_token(
        creds.credentials, consts.Auth.ACCESS_TOKEN_ATTRS
    )


def get_refresh_token(
    creds: HTTPAuthorizationCredentials = Depends(__http_bearer),
) -> str:
    """
    Получить refresh-токен
    :param creds: данные авторизации
    :return: refresh-токен
    """

    return token_validator.validate_token(
        creds.credentials, consts.Auth.REFRESH_TOKEN_ATTRS
    )
