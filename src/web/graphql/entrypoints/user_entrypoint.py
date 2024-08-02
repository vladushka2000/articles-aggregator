import uuid

import strawberry
from strawberry.fastapi import GraphQLRouter

from services import user_service
from tools import consts, jwt_helper
from web.graphql.dependencies import token_dependency
from web.graphql.models import user_models


@strawberry.type
class UserQuery:
    """
    Класс запроса через GraphQL на получение данных
    """

    @strawberry.field
    async def get_my_user_data(
        self, context_info: strawberry.Info[token_dependency.TokenDependency]
    ) -> user_models.UserModel:
        """
        Получить свои данные
        :param context_info: информация из контекста запроса
        :return: информация о пользователе
        """

        jwt_manager = jwt_helper.JWTHelper()
        access_token = context_info.context.get_access_token()
        payload = jwt_manager.get_payload_by_token(
            access_token, consts.Auth.ACCESS_TOKEN_ATTRS
        )

        return user_models.UserModel(
            id=payload["sub"],
            name=payload["user_name"],
            registration_date=payload["registration_date"],
        )

    @strawberry.field
    async def get_user_data(self, user_id: uuid.UUID) -> user_models.UserModel:
        """
        Получить данные о пользователе по идентификатору
        :param user_id: идентификатор пользователя
        :return: информация о пользователе
        """

        user = await user_service.UserService.get_user(user_id)

        return user_models.UserModel(
            id=user.id, name=user.name, registration_date=user.registration_date
        )


auth_schema = strawberry.Schema(query=UserQuery)
router = GraphQLRouter(
    auth_schema, "/users-graphql", context_getter=token_dependency.get_token
)
