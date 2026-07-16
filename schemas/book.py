from pydantic import BaseModel, ConfigDict, Field


class BookCreate(BaseModel):
    title: str = Field(..., max_length=200)
    isbn: str = Field(..., min_length=13, max_length=13)
    author_id: int
    category_ids: list[int]
    description: str | None = None
    published_year: int | None = None
    total_copies: int = Field(default=1, ge=1)


class BookPartialUpdate(BaseModel):
    title: str | None = None
    isbn: str | None = Field(
        default=None,
        min_length=13,
        max_length=13
    )
    author_id: int | None = None
    category_ids: list[int] | None = None
    description: str | None = None
    published_year: int | None = None
    total_copies: int | None = Field(
        default=None,
        ge=1
    )


class BookUpdate(BaseModel):
    title: str = Field(..., max_length=200)
    isbn: str = Field(
        ...,
        min_length=13,
        max_length=13,
    )
    author_id: int
    category_ids: list[int]
    description: str | None = None
    published_year: int | None = None
    total_copies: int = Field(
        ...,
        ge=1,
    )


class BookResponse(BaseModel):
    id: int
    title: str
    slug: str
    isbn: str
    author_id: int
    description: str | None
    cover_image: str | None
    total_copies: int
    available_copies: int
    published_year: int | None
    model_config = ConfigDict(
        from_attributes=True
    )