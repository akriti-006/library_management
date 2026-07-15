from datetime import datetime, date
from sqlalchemy import Date, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class BorrowRecord(Base):
    __tablename__= "borrow_records"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)
    member_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    borrowed_on: Mapped[date] = mapped_column(Date, default=date.today)
    due_date: Mapped[date] = mapped_column(Date,nullable=False)
    returned_on: Mapped[date | None] = mapped_column(Date,nullable=True)
    is_returned: Mapped[bool] = mapped_column(Boolean,default=False)
    book = relationship("Book",back_populates="borrow_records")
    member = relationship("User",back_populates="borrow_records")

    def __repr__(self):
        return f"<BorrowRecord {self.id}>"
