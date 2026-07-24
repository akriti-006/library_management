from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.pagination import PaginatedResponse

from database import get_db
from schemas.book import (
    BookCreate,
    BookUpdate,
    BookResponse,
    BookPartialUpdate
)
from services import book as book_service
from exceptions import (
    AlreadyExistsException,
    NotFoundException,
    ValidationException
)
from dependencies import get_current_user
from models.user import User

router = APIRouter(
    prefix="/books",
    tags=["Books"],
)


@router.post("/", response_model=BookResponse)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return book_service.create_book(db, book, current_user=current_user)

    except AlreadyExistsException as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        )

    except NotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except ValidationException as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    

@router.get("/", response_model=PaginatedResponse[BookResponse])
def get_books(
    search: str | None = None,
    author_id: int | None = None,
    category: str | None = None,
    available: bool | None = None,
    sort: str | None = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return book_service.get_all_books(
        db=db,
        search=search,
        author_id=author_id,
        category=category,
        available=available,
        sort=sort,
        page=page,
        limit=limit,
    )


@router.get("/{book_id}", response_model=BookResponse)
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
):
    book = book_service.get_book_by_id(
        db,
        book_id,
    )

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    return book


@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return book_service.update_book(
            db=db,
            book_id=book_id,
            book_data=book,
            current_user=current_user
        )

    except AlreadyExistsException as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        )

    except NotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except ValidationException as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    

@router.patch("/{book_id}", response_model=BookResponse)
def partial_update_book(
    book_id: int,
    book: BookPartialUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return book_service.partial_update_book(
            db=db,
            book_id=book_id,
            book_data=book,
            current_user=current_user
        )

    except AlreadyExistsException as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        )

    except NotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except ValidationException as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    

@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        book_service.delete_book(
            db=db,
            book_id=book_id,
            current_user=current_user
        )

        return {
            "message": "Book deleted successfully"
        }

    except NotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
