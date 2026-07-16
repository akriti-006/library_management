from pydantic import BaseModel, ConfigDict
from typing import Generic, TypeVar
from pydantic.generics import GenericModel

T = TypeVar("T")


class PaginatedResponse(GenericModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    limit: int
    total_pages: int
    model_config = ConfigDict(
        from_attributes=True
    )