import uuid

from fastapi import APIRouter, Depends

from services import user_service
from tools import consts, jwt_helper
from web.fast_api.dependencies import token_dependency
from web.fast_api.models.user import user_model

router = APIRouter(prefix="/users")


@router.get("/me")
async def get_my_user_data(
    access_token: str = Depends(token_dependency.get_access_token),
) -> user_model.UserModel:
    """
    Получить свои данные
    :param access_token: access-токен
    :return: информация о пользователе
    """

    jwt_manager = jwt_helper.JWTHelper()
    payload = jwt_manager.get_payload_by_token(
        access_token, consts.Auth.ACCESS_TOKEN_ATTRS
    )

    return user_model.UserModel(
        id=payload["sub"],
        name=payload["user_name"],
        registration_date=payload["registration_date"],
    )


@router.get("/{user_id}")
async def get_user_data(user_id: uuid.UUID) -> user_model.UserModel:
    """
    Получить данные о пользователе по идентификатору
    :param user_id: идентификатор пользователя
    :return: информация о пользователе
    """

    user = await user_service.UserService.get_user(user_id)

    return user_model.UserModel(
        id=user.id, name=user.name, registration_date=user.registration_date
    )
