import strawberry


@strawberry.input
class AuthInput:
    """
    Модель для регистрации и входа пользователя в систему
    """

    name: str
    password: str


@strawberry.type
class JWTModel:
    """
    Модель данных JWT-токенов
    """

    access_token: str
    refresh_token: str
