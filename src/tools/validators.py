import string

from tools import consts


def validate_password(password: str) -> str:
    """
    Провалидировать пароль
    :param password: пароль
    :return: пароль, в случае удачной валидации
    """

    if (
        len(password) < consts.Auth.MIN_PASSWORD_LENGTH
        or len(password) > consts.Auth.MAX_PASSWORD_LENGTH
        or not any(char.isdigit() for char in password)
        or not any(char.isupper() for char in password)
        or not any(char.islower() for char in password)
    ):
        raise ValueError("Пароль не удовлетворяет условиям")

    return password


def validate_name(name: str) -> str:
    """
    Провалидировать имя пользователя
    :param name: имя
    :return: имя пользователя, в случае удачной валидации
    """

    if (
        len(name) < consts.Auth.MIN_USERNAME_LENGTH
        or len(name) > consts.Auth.MAX_USERNAME_LENGTH
        or not any(char in string.ascii_letters for char in name)
    ):
        raise ValueError("Имя пользователя не удовлетворяет условиям")

    return name
