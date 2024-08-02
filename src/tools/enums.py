import enum
import uuid

from abstracts import abstract_enum


class AppWorkingMode(enum.Enum):
    """
    Enum режима работы приложения
    """

    REST = "REST"
    GRAPHQL = "GraphQl"


class RepositoryName(enum.Enum):
    """
    Enum названий репозиториев
    """

    ARTICLE_ALCHEMY_REPOSITORY = "article_alchemy_repository"
    ARTICLE_REDIS_REPOSITORY = "article_redis_repository"
    USER_REPOSITORY = "user_repository"
    TOKEN_REPOSITORY = "token_repository"
    TOPIC_REPOSITORY = "topic_repository"


class UOWName(enum.Enum):
    """
    Enum названий UOW
    """

    ALCHEMY_UOW = "alchemy_uow"
    REDIS_UOW = "redis_uow"


class PasswordHasherAlgorithm(enum.Enum):
    """
    Enum алгоритмов хеширования паролей
    """

    BCRYPT = "bcrypt"


class JWTAlgorithm(enum.Enum):
    """
    Enum алгоритмов хеширования jwt-токена
    """

    HS256 = "HS256"


class TokenType(enum.Enum):
    """
    Enum типа токена
    """

    ACCESS = "access"
    REFRESH = "refresh"


class ArticleTopic(abstract_enum.AbstractIdNameEnum):
    """
    Enum тем для статей
    """

    TECH = (uuid.UUID("b1935073-7f62-4c49-8dd6-443fcc2451ab"), "Техническая")
    SCIENCE = (uuid.UUID("81dec9ae-f59f-4ee4-b817-ffa3bf9d6f92"), "Научная")
    NEWS = (uuid.UUID("2a20d146-76ed-463c-a7aa-d344710077e3"), "Новостная")
