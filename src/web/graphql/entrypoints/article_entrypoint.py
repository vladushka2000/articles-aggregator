import uuid

import strawberry
from strawberry.fastapi import GraphQLRouter

from dto import article_dto, user_dto
from services import article_service
from tools import consts, jwt_helper
from web.graphql.dependencies import token_dependency
from web.graphql.models import article_models, user_models


@strawberry.type
class ArticleQuery:
    """
    Класс запроса через GraphQL на получение данных
    """

    @strawberry.field
    async def get_article_by_id(
        self, article_id: uuid.UUID
    ) -> article_models.ArticleType:
        """
        Получить запись статьи по ее идентификатору
        :param article_id: идентификатор статьи
        :return: данные полученной статьи
        """

        article_result = await article_service.ArticleService.retrieve_article(
            article_id
        )

        return article_models.ArticleType(
            id=article_result.id,
            user=user_models.UserModelBase(
                id=article_result.user_id, name=article_result.user_name
            ),
            creation_date=article_result.creation_date,
            topic=article_models.TopicType(
                id=article_result.topic_id, name=article_result.topic_name
            ),
            text=article_result.text,
            views=article_result.views,
        )

    @strawberry.field
    async def get_popular_articles(self) -> list[article_models.ArticleType]:
        """
        Получить популярные статьи
        :return: список популярных статей
        """

        articles_result = (
            await article_service.ArticleService.retrieve_popular_articles()
        )

        return [
            article_models.ArticleType(
                id=article.id,
                user=user_models.UserModelBase(
                    id=article.user_id, name=article.user_name
                ),
                creation_date=article.creation_date,
                topic=article_models.TopicType(
                    id=article.topic_id, name=article.topic_name
                ),
                text=article.text,
                views=article.views,
            )
            for article in articles_result
        ]


@strawberry.type
class ArticleMutation:
    """
    Класс запроса через GraphQL на создание и изменение данных
    """

    @strawberry.field
    async def create_article(
        self,
        article_info: article_models.ArticleCreateInput,
        context_info: strawberry.Info[token_dependency.TokenDependency],
    ) -> article_models.ArticleType:
        """
        Создать запись статьи
        :param article_info: исходные данные для создания статьи
        :param context_info: информация из контекста запроса
        :return: данные полученной статьи
        """

        token = context_info.context.get_access_token()

        jwt_manager = jwt_helper.JWTHelper()
        payload = jwt_manager.get_payload_by_token(
            token, consts.Auth.ACCESS_TOKEN_ATTRS
        )

        user = user_dto.UserInfoDTO(id=payload["sub"], name=payload["user_name"])
        article = article_dto.ArticleCreateDTO(
            id=uuid.uuid4(),
            user_id=user.id,
            topic_id=article_info.topic_id,
            text=article_info.text,
        )

        article_result = await article_service.ArticleService.create_article(
            user, article
        )

        return article_models.ArticleType(
            id=article_result.id,
            user=user_models.UserModelBase(
                id=article_result.user_id, name=article_result.user_name
            ),
            creation_date=article_result.creation_date,
            topic=article_models.TopicType(
                id=article_result.topic_id, name=article_result.topic_name
            ),
            text=article_result.text,
            views=article_result.views,
        )

    @strawberry.field
    async def update_article(
        self,
        article_info: article_models.ArticleUpdateInput,
        context_info: strawberry.Info[token_dependency.TokenDependency],
    ) -> article_models.ArticleType:
        """
        Обновить запись статьи
        :param article_info: исходные данные для обновления статьи
        :param context_info: информация из контекста запроса
        :return: данные полученной статьи
        """

        token = context_info.context.get_access_token()

        jwt_manager = jwt_helper.JWTHelper()
        payload = jwt_manager.get_payload_by_token(
            token, consts.Auth.ACCESS_TOKEN_ATTRS
        )

        user = user_dto.UserInfoDTO(id=payload["sub"], name=payload["user_name"])
        article = article_dto.ArticleUpdateDTO(
            id=article_info.id,
            user_id=user.id,
            topic_id=article_info.topic_id,
            text=article_info.text,
        )

        article_result = await article_service.ArticleService.update_article(
            user, article
        )

        return article_models.ArticleType(
            id=article_result.id,
            user=user_models.UserModelBase(
                id=article_result.user_id, name=article_result.user_name
            ),
            creation_date=article_result.creation_date,
            topic=article_models.TopicType(
                id=article_result.topic_id, name=article_result.topic_name
            ),
            text=article_result.text,
            views=article_result.views,
        )


article_schema = strawberry.Schema(query=ArticleQuery, mutation=ArticleMutation)
router = GraphQLRouter(
    article_schema, "/articles-graphql", context_getter=token_dependency.get_token
)
