from sqlalchemy import Table, Column, ForeignKey

from database import Base


book_category = Table(
    "book_category",
    Base.metadata,

    Column(
        "book_id",
        ForeignKey("books.id"),
        primary_key=True
    ),

    Column(
        "category_id",
        ForeignKey("categories.id"),
        primary_key=True
    ),
)