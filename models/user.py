from datetime import datetime
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__= "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(50), nullable=False)
    is_staff: Mapped[str] = mapped_column(Boolean, default=False)
    created_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    borrow_records = relationship( "BorrowRecord", back_populates="member", cascade="all, delete-orphan" )
    