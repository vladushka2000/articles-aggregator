from graphql import ValidationRule

from tools import validators


class AuthRule(ValidationRule):
    """
    Класс правил валидации для процесса аутентификации
    """

    def validate_name(self, node, *args) -> None:
        """
        Провалидировать имя пользователя
        :param node: объект данных GraphQL
        """

        validators.validate_name(node.name)

    def validate_password(self, node, *args) -> None:
        """
        Провалидировать пароль
        :param node: объект данных GraphQL
        """

        validators.validate_password(node.password)
