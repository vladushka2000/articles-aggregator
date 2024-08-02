import uuid

from fastapi import APIRouter, Depends, Query

from dto import article_dto, user_dto
from services import article_service
from tools import consts, jwt_helper
from web.fast_api.dependencies import token_dependency
from web.fast_api.models.articles import article_model

router = APIRouter(prefix="/articles")


@router.post("/create")
async def create_article(
    article_schema: article_model.ArticleWriteModel,
    access_token: str = Depends(token_dependency.get_access_token),
) -> article_model.ArticleResultModel:
    """
    Создать статью
    :param article_schema: исходные данные для создания статьи
    :param access_token: access-токен
    :return: данные созданной статьи
    """

    jwt_manager = jwt_helper.JWTHelper()
    payload = jwt_manager.get_payload_by_token(
        access_token, consts.Auth.ACCESS_TOKEN_ATTRS
    )

    user = user_dto.UserInfoDTO(id=payload["sub"], name=payload["user_name"])

    article = article_dto.ArticleCreateDTO(
        id=uuid.uuid4(),
        user_id=user.id,
        topic_id=article_schema.topic_id,
        text=article_schema.text,
    )

    article_result = await article_service.ArticleService.create_article(user, article)

    return article_model.ArticleResultModel(
        id=article_result.id,
        user_id=article_result.user_id,
        user_name=article_result.user_name,
        creation_date=article_result.creation_date,
        topic_id=article_result.topic_id,
        topic_name=article_result.topic_name,
        text=article_result.text,
        views=article_result.views,
    )


@router.get("/popular")
async def retrieve_popular_articles() -> list[article_model.ArticleResultModel]:
    """
    Получить популярные статьи
    :return: данные полученных статьей
    """

    articles_result = await article_service.ArticleService.retrieve_popular_articles()

    return [
        article_model.ArticleResultModel(
            id=article.id,
            user_id=article.user_id,
            user_name=article.user_name,
            creation_date=article.creation_date,
            topic_id=article.topic_id,
            topic_name=article.topic_name,
            text=article.text,
            views=article.views,
        )
        for article in articles_result
    ]


@router.get("/{article_id}")
async def retrieve_article(article_id: uuid.UUID) -> article_model.ArticleResultModel:
    """
    Получить статью
    :param article_id: идентификатор статьи
    :return: данные полученной статьи
    """

    article_result = await article_service.ArticleService.retrieve_article(article_id)

    return article_model.ArticleResultModel(
        id=article_result.id,
        user_id=article_result.user_id,
        user_name=article_result.user_name,
        creation_date=article_result.creation_date,
        topic_id=article_result.topic_id,
        topic_name=article_result.topic_name,
        text=article_result.text,
        views=article_result.views,
    )


@router.patch("/update")
async def update_article(
    article_schema: article_model.ArticleUpdateModel,
    access_token: str = Depends(token_dependency.get_access_token),
) -> article_model.ArticleResultModel:
    """
    Обновить статью
    :param article_schema: исходные данные для обновления статьи
    :param access_token: access-токен
    :return: данные обновленной статьи
    """

    jwt_manager = jwt_helper.JWTHelper()
    payload = jwt_manager.get_payload_by_token(
        access_token, consts.Auth.ACCESS_TOKEN_ATTRS
    )

    user = user_dto.UserInfoDTO(id=payload["sub"], name=payload["user_name"])

    article = article_dto.ArticleUpdateDTO(
        id=article_schema.id,
        user_id=user.id,
        topic_id=article_schema.topic_id,
        text=article_schema.text,
    )

    article_result = await article_service.ArticleService.update_article(user, article)

    return article_model.ArticleResultModel(
        id=article_result.id,
        user_id=article_result.user_id,
        user_name=article_result.user_name,
        creation_date=article_result.creation_date,
        topic_id=article_result.topic_id,
        topic_name=article_result.topic_name,
        text=article_result.text,
        views=article_result.views,
    )


@router.delete("/delete")
async def delete_article(
    article_id: uuid.UUID = Query(alias="id"),
    access_token: str = Depends(token_dependency.get_access_token),
) -> None:
    """
    Удалить статью
    :param article_id: идентификатор статьи
    :param access_token: access-токен
    :return: данные обновленной статьи
    """

    jwt_manager = jwt_helper.JWTHelper()
    payload = jwt_manager.get_payload_by_token(
        access_token, consts.Auth.ACCESS_TOKEN_ATTRS
    )

    user = user_dto.UserInfoDTO(id=payload["sub"], name=payload["user_name"])

    await article_service.ArticleService.delete_article(user, article_id)
