from passlib import context

from tools import enums


class PasswordHelper:
    """
    Класс, содержащий вспомогательные функции для работы с паролями
    """

    def __init__(self, hash_algorithm: enums.PasswordHasherAlgorithm) -> None:
        """
        Инициализировать переменные
        :param hash_algorithm: алгоритм хеширования пароля
        """

        self.hasher = context.CryptContext(schemes=[hash_algorithm.value])

    def encode_password(self, password: str) -> str:
        """
        Закодировать пароль
        :param password: пароль
        :return: закодированный пароль
        """

        return self.hasher.hash(password)

    def is_password_valid(self, password: str, encoded_password: str) -> bool:
        """
        Проверить, соответствует ли пароль закодирвоанному
        :param password: пароль
        :param encoded_password: закодированный пароль
        :return: True, если пароли совпадают, иначе - False
        """

        return self.hasher.verify(password, encoded_password)
