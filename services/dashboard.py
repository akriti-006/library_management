from sqlalchemy import func
from sqlalchemy.orm import Session

from models.author import Author
from models.book import Book
from models.borrow import BorrowRecord
from models.category import Category
from models.user import User


def get_dashboard(db: Session):

    total_books = db.query(func.count(Book.id)).scalar()

    available_books = (
        db.query(func.sum(Book.available_copies))
        .scalar() or 0
    )

    borrowed_books = (
        db.query(func.sum(Book.total_copies - Book.available_copies))
        .scalar() or 0
    )

    total_members = db.query(func.count(User.id)).scalar()

    active_borrow_records = (
        db.query(func.count(BorrowRecord.id))
        .filter(BorrowRecord.is_returned == False)
        .scalar()
    )

    returned_books = (
        db.query(func.count(BorrowRecord.id))
        .filter(BorrowRecord.is_returned == True)
        .scalar()
    )

    total_authors = db.query(func.count(Author.id)).scalar()

    total_categories = db.query(func.count(Category.id)).scalar()

    return {
        "total_books": total_books,
        "available_books": available_books,
        "borrowed_books": borrowed_books,
        "total_members": total_members,
        "active_borrow_records": active_borrow_records,
        "returned_books": returned_books,
        "total_authors": total_authors,
        "total_categories": total_categories,
    }