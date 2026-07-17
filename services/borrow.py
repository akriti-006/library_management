from datetime import date, timedelta

from sqlalchemy.orm import Session

from exceptions import (
    AlreadyExistsException,
    NotFoundException,
    ValidationException,
)
from models.book import Book
from models.borrow import BorrowRecord
from models.user import User
from services.fine import calculate_fine


def borrow_book(
    db: Session,
    current_user: User,
    book_id: int,
):
    # Check if book exists
    book = (
        db.query(Book)
        .filter(Book.id == book_id)
        .first()
    )

    if book is None:
        raise NotFoundException(
            "Book not found."
        )

    # Check availability
    if book.available_copies <= 0:
        raise ValidationException(
            "Book is currently unavailable."
        )

    # Check if user already borrowed this book
    existing = (
        db.query(BorrowRecord)
        .filter(
            BorrowRecord.book_id == book_id,
            BorrowRecord.member_id == current_user.id,
            BorrowRecord.is_returned == False,
        )
        .first()
    )

    if existing:
        raise AlreadyExistsException(
            "You have already borrowed this book."
        )

    borrow = BorrowRecord(
        book_id=book.id,
        member_id=current_user.id,
        borrowed_on=date.today(),
        due_date=date.today() + timedelta(days=14),
        is_returned=False,
    )

    db.add(borrow)

    # Decrease available copies
    book.available_copies -= 1

    db.commit()
    db.refresh(borrow)

    return borrow


def return_book(
    db: Session,
    current_user: User,
    borrow_id: int,
):
    borrow = (
        db.query(BorrowRecord)
        .filter(BorrowRecord.id == borrow_id)
        .first()
    )

    if borrow is None:
        raise NotFoundException(
            "Borrow record not found."
        )

    if borrow.is_returned:
        raise ValidationException(
            "Book has already been returned."
        )
    
    if borrow.member_id != current_user.id:
        raise ValidationException(
            "You can only return your own borrowed books."
        )

    borrow.returned_on = date.today()
    borrow.is_returned = True

    borrow.book.available_copies += 1

    fine = calculate_fine(
        borrow.due_date,
        borrow.returned_on,
    )

    db.commit()
    db.refresh(borrow)

    return {
        "message": "Book returned successfully.",
        "borrow_record": borrow,
        "late_days": fine["late_days"],
        "fine_amount": fine["fine_amount"],
    }


def get_my_borrowed_books(
    db: Session,
    current_user: User,
):
    borrow_records = (
        db.query(BorrowRecord)
        .filter(
            BorrowRecord.member_id == current_user.id,
            BorrowRecord.is_returned == False,
        )
        .all()
    )

    return borrow_records


def get_borrow_history(
    db: Session,
    current_user: User,
):
    borrow_records = (
        db.query(BorrowRecord)
        .filter(
            BorrowRecord.member_id == current_user.id
        )
        .order_by(
            BorrowRecord.borrowed_on.desc()
        )
        .all()
    )

    return borrow_records
