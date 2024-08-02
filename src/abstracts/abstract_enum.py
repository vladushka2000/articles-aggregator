import enum
import uuid


class AbstractIdNameEnum(enum.Enum):
    """
    Абстрактный класс Enum для хранения иденьтификатора и названия
    """

    def __new__(cls, id_: uuid.UUID, value: str) -> enum.Enum:
        """
        Конструктор класса
        :param id_: идентификатор элемента Enum
        :param value: название элемента Enum
        """

        obj = object.__new__(cls)
        obj._value_ = value
        obj.id = id_

        return obj
