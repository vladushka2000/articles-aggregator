import uuid

from pydantic import Field

from abstracts import base_dto


class TopicDTO(base_dto.PydanticBase):
    """
    DTO, содержащий данные о теме статьи
    """

    id: uuid.UUID = Field(description="Идентификатор статьи")
    name: str = Field(description="Название темы статьи")
