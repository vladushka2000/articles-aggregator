import datetime

import jwt
from jwt.exceptions import InvalidTokenError

from dto import token_dto, user_dto
from tools import app_config, enums

config = app_config.config


class JWTHelper:
    """
    Класс, содержащий вспомогательные методы для работы с JWT-токенами
    """

    def _create_payload(
        self, user_data: user_dto.UserDTO, token_params: token_dto.TokenAttrsDTO
    ) -> dict:
        """
        Создать полезную нагрузку
        :param user_data: информация о пользователе
        :param token_params: параметры токена
        :return: полезная нагрузка
        """

        current_time = datetime.datetime.now()
        expire = (
            current_time
            + datetime.timedelta(seconds=token_params.expiration_time_in_sec)
        ).timestamp()

        payload = {
            "sub": str(user_data.id),
            "iat": int(current_time.timestamp()),
            "scope": token_params.token_type.value,
            "exp": int(expire),
        }

        if token_params.token_type == enums.TokenType.ACCESS:
            payload.update(
                {
                    "user_name": user_data.name,
                    "registration_date": int(user_data.registration_date.timestamp()),
                }
            )

        return payload

    def _encode_jwt(self, payload: dict) -> str:
        """
        Закодировать JWT-токен
        :param payload: информация для кодирования
        :return: JWT-токен
        """

        return jwt.encode(
            payload.copy(),
            config.secret_key,
            config.jwt_algorithm.value,
        )

    def _decode_jwt(self, token: str) -> dict:
        """
        Раскодировать JWT-токена
        :param token: токен для декодирования
        :return: информация из JWT-токена
        """

        return jwt.decode(token, config.secret_key, [config.jwt_algorithm.value])

    def issue_jwt(
        self, user: user_dto.UserDTO, token_params: token_dto.TokenAttrsDTO
    ) -> str:
        """
        Выпустить JWT-токен.

        :param user: данные пользователя
        :param token_params: параметры токена
        :return: JWT-токен
        """

        payload = self._create_payload(user, token_params)

        return self._encode_jwt(payload)

    def is_jwt_token_expired(self, payload: dict, expire_time_in_sec: int) -> bool:
        """
        Рассчитать, истек ли срок жизни токена
        :param payload: payload токена
        :param expire_time_in_sec: время жизни токена в секундах
        :return: True, если срок жизни токена истек, иначе - False
        """

        try:
            payload_expire = datetime.datetime.fromtimestamp(payload["exp"])

            if (
                abs(datetime.datetime.now() - payload_expire).seconds
                >= expire_time_in_sec
            ):
                return True

            return False
        except InvalidTokenError:
            raise

    def get_payload_by_token(
        self, token: str, token_params: token_dto.TokenAttrsDTO
    ) -> dict:
        """
        Получить полезную нагрузку из JWT-токена
        :param token: токен
        :param token_params: параметры токена
        :return: полезная нагрузка
        """

        payload = self._decode_jwt(token=token)

        if payload[
            "scope"
        ] != token_params.token_type.value or self.is_jwt_token_expired(
            payload, token_params.expiration_time_in_sec
        ):
            raise InvalidTokenError

        return payload
