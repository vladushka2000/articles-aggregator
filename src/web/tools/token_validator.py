from fastapi import status, HTTPException

from dto import token_dto
from tools import jwt_helper


def validate_token(token: str, token_type: token_dto.TokenAttrsDTO) -> str:
    """
    Валидировать токен
    :param token: данные авторизации
    :param token_type: параметры токена
    :return: токен
    """

    jwt_manager = jwt_helper.JWTHelper()
    payload = jwt_manager.get_payload_by_token(token, token_type)

    if jwt_manager.is_jwt_token_expired(payload, token_type.expiration_time_in_sec):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return token
