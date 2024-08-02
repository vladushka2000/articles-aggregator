from pydantic import BaseModel, ConfigDict


class PydanticBase(BaseModel):
    """
    Базовая модель для моделей pydantic
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
