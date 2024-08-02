import strawberry
from strawberry.fastapi import GraphQLRouter

from dto import auth_dto
from services import auth_service
from web.graphql.dependencies import token_dependency
from web.graphql.models import auth_models


@strawberry.type
class AuthMutation:
    """
    Класс запроса через GraphQL на создание и изменение данных
    """

    @strawberry.field
    async def sign_up(
        self,
        user_init_data: auth_models.AuthInput,
    ) -> auth_models.JWTModel:
        """
        Зарегистрироваться в приложении
        :param user_init_data: данные пользователя
        :return: токены
        """

        user = auth_dto.AuthDTO(
            name=user_init_data.name, password=user_init_data.password
        )

        tokens = await auth_service.AuthService.sign_up_user(user)

        return auth_models.JWTModel(
            access_token=tokens.access_token, refresh_token=tokens.refresh_token
        )


@strawberry.type
class AuthQuery:
    """
    Класс запроса через GraphQL на получение данных
    """

    @strawberry.field
    async def sign_in(
        self, user_init_data: auth_models.AuthInput
    ) -> auth_models.JWTModel:
        """
        Войти в приложение
        :param user_init_data: данные пользователя
        :return: токены
        """

        user = auth_dto.AuthDTO(
            name=user_init_data.name, password=user_init_data.password
        )

        tokens = await auth_service.AuthService.sign_in_user(user)

        return auth_models.JWTModel(
            access_token=tokens.access_token, refresh_token=tokens.refresh_token
        )

    @strawberry.field
    async def refresh_tokens(
        self, context_info: strawberry.Info[token_dependency.TokenDependency]
    ) -> auth_models.JWTModel:
        """
        Обновить токены
        :param context_info: информация из контекста запроса
        :return: обновленные access и refresh-токены
        """

        refresh_token = context_info.context.get_refresh_token()
        tokens = await auth_service.AuthService.refresh_tokens(refresh_token)

        return auth_models.JWTModel(
            access_token=tokens.access_token, refresh_token=tokens.refresh_token
        )


auth_schema = strawberry.Schema(query=AuthQuery, mutation=AuthMutation)
router = GraphQLRouter(
    auth_schema, "/auth-graphql", context_getter=token_dependency.get_token
)
