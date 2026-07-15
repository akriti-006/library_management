from datetime import datetime
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

from .book_category import book_category


class Book(Base):
    __tablename__= "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[int] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    isbn: Mapped[str] = mapped_column(String(13), unique=True, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)
    description: Mapped[str|None] = mapped_column(Text, nullable=True)
    cover_image: Mapped[str|None] = mapped_column(String(255), nullable=True)
    total_copies: Mapped[int] = mapped_column(Integer, default=1)
    available_copies: Mapped[int] = mapped_column(Integer, default=1)
    published_year: Mapped[int|None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author = relationship("Author", back_populates="books")
    categories = relationship("Category", secondary=book_category, back_populates="books")
    borrow_records = relationship("BorrowRecord", back_populates="book")

    def __repr__(self):
        return f"<Book {self.title}>"
