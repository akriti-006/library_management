from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .book_category import book_category
from database import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100),unique=True,nullable=False)
    slug: Mapped[str] = mapped_column(String(100),unique=True,nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

    books = relationship( "Book", secondary=book_category, back_populates="categories" )

    def __repr__(self):
        return f"<Category {self.name}>"