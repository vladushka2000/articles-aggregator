from dto import token_dto
from tools import app_config, enums

config = app_config.config


class Articles:
    """
    Константы, связанные со статьями
    """

    MAX_ARTICLE_LENGTH = 10_000
    MOST_VIEWED_ARTICLE_LIFETIME_IN_SEC = 86400
    POPULAR_ARTICLES_COUNT = 10
    DATETIME_STRING_FORMAT = "%Y.%m.%d %H:%M:%S"


class Auth:
    """
    Константы, связанные с аутентификацией
    """

    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 20
    MIN_PASSWORD_LENGTH = 5
    MAX_PASSWORD_LENGTH = 20

    ACCESS_TOKEN_ATTRS = token_dto.TokenAttrsDTO(
        token_type=enums.TokenType.ACCESS,
        expiration_time_in_sec=config.access_token_expire_in_sec,
    )
    REFRESH_TOKEN_ATTRS = token_dto.TokenAttrsDTO(
        token_type=enums.TokenType.REFRESH,
        expiration_time_in_sec=config.refresh_token_expire_in_sec,
    )
