from datetime import date

from sqlalchemy import String, Text, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(100),nullable=False)
    bio: Mapped[str | None] = mapped_column(Text,nullable=True)
    date_of_birth: Mapped[date | None] = mapped_column(Date,nullable=True)
    photo: Mapped[str | None] = mapped_column(String(255),nullable=True)

    books = relationship( "Book", back_populates="author" )

    def __repr__(self):
        return f"<Author {self.full_name}>"