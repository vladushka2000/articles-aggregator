import datetime

from abstracts import abstract_repository as abs_repo
from dto import token_dto


class TokenRepository(
    abs_repo.AbstractRedisRepository,
    abs_repo.CreateMixin,
    abs_repo.RetrieveMixin,
    abs_repo.DeleteMixin,
):
    """
    Репозиторий для работы с токенами
    """

    async def create(
        self,
        token: token_dto.UsersRefreshToken,
        expiration_in_seconds: datetime.timedelta | None = None,
    ) -> None:
        """
        Создать запись о пользователе и его refresh-токене
        :param token: объект данных о пользователе и его refresh-токене
        :param expiration_in_seconds: время жизни записи
        """

        await self.session.set(
            token.user_id, token.refresh_token, expiration_in_seconds
        )

    async def retrieve(
        self,
        user_id: str,
    ) -> str | None:
        """
        Получить refresh-токен
        :param user_id: идентификатор пользователя
        :return: запись в БД в случае нахождения, иначе - None
        """

        return await self.session.get(user_id)

    async def delete(self, user_id: str) -> None:
        """
        Удалить refresh-токен
        :param user_id: идентификатор пользователя
        """

        return await self.session.delete(user_id)
