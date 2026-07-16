from sqlalchemy.orm import Session

from models.author import Author
from models.book import Book
from models.category import Category
from slugify import slugify

from models.book import Book
from schemas.book import BookCreate, BookUpdate, BookPartialUpdate
from exceptions import (
    AlreadyExistsException,
    NotFoundException,
    ValidationException,
)
from services import author as author_service
from services import category as category_service
from sqlalchemy import or_


def get_book_by_id(
    db: Session,
    book_id: int
):
    return (
        db.query(Book)
        .filter(Book.id == book_id)
        .first()
    )


def get_book_by_isbn(
    db: Session,
    isbn: str
):
    return (
        db.query(Book)
        .filter(Book.isbn == isbn)
        .first()
    )


def get_author_by_id(
    db: Session,
    author_id: int
):
    return (
        db.query(Author)
        .filter(Author.id == author_id)
        .first()
    )


def get_categories_by_ids(
    db: Session,
    category_ids: list[int]
):
    return (
        db.query(Category)
        .filter(Category.id.in_(category_ids))
        .all()
    )


def validate_categories(
    db: Session,
    category_ids: list[int]
):
    """
    Validate that all category IDs exist.
    Returns the list of Category objects if valid,
    otherwise returns None.
    """
    categories = category_service.get_categories_by_ids(
        db,
        category_ids
    )

    if len(categories) != len(category_ids):
        return None

    return categories


def create_book(
    db: Session,
    book_data: BookCreate
):
    # Check if ISBN already exists
    if get_book_by_isbn(db, book_data.isbn):
        raise AlreadyExistsException(
            "Book with this ISBN already exists"
        )

    # Check if author exists
    author = author_service.get_author_by_id(db, book_data.author_id)

    if author is None:
        raise NotFoundException("Author not found")

    # Validate categories
    categories = validate_categories(
        db,
        book_data.category_ids
    )

    if categories is None:
        raise ValidationException("One or more categories do not exist")

    # Create book
    book = Book(
        title=book_data.title,
        slug=slugify(book_data.title),
        isbn=book_data.isbn,
        description=book_data.description,
        published_year=book_data.published_year,
        total_copies=book_data.total_copies,
        available_copies=book_data.total_copies,
        author_id=book_data.author_id,
    )

    # Attach categories
    book.categories = categories

    db.add(book)
    db.commit()
    db.refresh(book)

    return book


def get_all_books(
    db: Session,
    search: str | None = None,
    author_id: int | None = None,
    category_id: int | None = None,
    page: int = 1,
    limit: int = 10,
):
    query = db.query(Book)

    # Search by title or ISBN
    if search:
        query = query.filter(
            or_(
                Book.title.ilike(f"%{search}%"),
                Book.isbn.ilike(f"%{search}%"),
            )
        )

    # Filter by author
    if author_id:
        query = query.filter(
            Book.author_id == author_id
        )

    # Filter by category
    if category_id:
        query = query.filter(
            Book.categories.any(id=category_id)
        )

    # Pagination
    offset = (page - 1) * limit

    total = query.count()

    books = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    total_pages = (
        total + limit - 1
    ) // limit

    return {
        "items": books,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
    }


def update_book(
    db: Session,
    book_id: int,
    book_data: BookUpdate,
):
    # Find the book
    book = get_book_by_id(db, book_id)

    if book is None:
        raise NotFoundException("Book not found")

    # Check if ISBN has changed
    if book.isbn != book_data.isbn:
        existing_book = get_book_by_isbn(
            db,
            book_data.isbn,
        )

        if existing_book:
            raise AlreadyExistsException(
                "Book with this ISBN already exists"
            )

    # Validate author
    author = get_author_by_id(
        db,
        book_data.author_id,
    )

    if author is None:
        raise NotFoundException(
            "Author not found"
        )

    # Validate categories
    categories = validate_categories(
        db,
        book_data.category_ids,
    )

    if categories is None:
        raise ValidationException(
            "One or more categories do not exist"
        )

    # Calculate borrowed books
    borrowed_books = (
        book.total_copies -
        book.available_copies
    )

    # Prevent invalid total copies
    if book_data.total_copies < borrowed_books:
        raise ValidationException(
            "Total copies cannot be less than borrowed books."
        )

    # Update available copies
    book.available_copies = (
        book_data.total_copies -
        borrowed_books
    )

    # Update remaining fields
    book.title = book_data.title
    book.slug = slugify(book_data.title)
    book.isbn = book_data.isbn
    book.author_id = book_data.author_id
    book.description = book_data.description
    book.published_year = book_data.published_year
    book.total_copies = book_data.total_copies

    # Update many-to-many relationship
    book.categories = categories

    db.commit()
    db.refresh(book)

    return book


def partial_update_book(
    db: Session,
    book_id: int,
    book_data: BookPartialUpdate,
):
    # Find the book
    book = get_book_by_id(
        db,
        book_id,
    )

    if book is None:
        raise NotFoundException(
            "Book not found"
        )

    # Only get fields sent by the client
    update_data = book_data.model_dump(
        exclude_unset=True
    )

    # Check ISBN
    if "isbn" in update_data:
        existing_book = get_book_by_isbn(
            db,
            update_data["isbn"],
        )

        if (
            existing_book
            and existing_book.id != book.id
        ):
            raise AlreadyExistsException(
                "Book with this ISBN already exists"
            )

    # Check Author
    if "author_id" in update_data:
        author = get_author_by_id(
            db,
            update_data["author_id"],
        )

        if author is None:
            raise NotFoundException(
                "Author not found"
            )

    # Check Categories
    if "category_ids" in update_data:
        categories = validate_categories(
            db,
            update_data["category_ids"],
        )

        if categories is None:
            raise ValidationException(
                "One or more categories do not exist"
            )

        book.categories = categories

    # Handle total copies
    if "total_copies" in update_data:
        borrowed_books = (
            book.total_copies -
            book.available_copies
        )

        if (
            update_data["total_copies"]
            < borrowed_books
        ):
            raise ValidationException(
                "Total copies cannot be less than borrowed books."
            )

        book.available_copies = (
            update_data["total_copies"]
            - borrowed_books
        )

    # Update remaining fields
    for key, value in update_data.items():

        if key == "category_ids":
            continue

        setattr(
            book,
            key,
            value,
        )

    # Update slug if title changed
    if "title" in update_data:
        book.slug = slugify(
            book.title
        )

    db.commit()
    db.refresh(book)

    return book


def delete_book(
    db: Session,
    book_id: int,
):
    book = get_book_by_id(
        db,
        book_id,
    )

    if book is None:
        raise NotFoundException(
            "Book not found"
        )

    db.delete(book)
    db.commit()