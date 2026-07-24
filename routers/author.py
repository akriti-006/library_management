from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.author import (
    AuthorCreate,
    AuthorResponse,
    AuthorUpdate,
)

from services import author as author_service
from dependencies import get_current_user
from models.user import User

router = APIRouter(
    prefix="/authors",
    tags=["Authors"]
)


@router.post("/", response_model=AuthorResponse)
def create_author(
    author: AuthorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return author_service.create_author(db, author, current_user=current_user)


@router.get("/", response_model=list[AuthorResponse])
def get_authors(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return author_service.get_all_authors(db, current_user=current_user)


@router.get("/{author_id}", response_model=AuthorResponse)
def get_author(
    author_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    author = author_service.get_author_by_id(db, author_id, current_user=current_user)

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    return author


@router.put("/{author_id}", response_model=AuthorResponse)
def update_author(
    author_id: int,
    author_data: AuthorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    author = author_service.get_author_by_id(db, author_id, current_user=current_user)

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    return author_service.update_author(
        db,
        author,
        author_data
    )


@router.patch("/{author_id}", response_model=AuthorResponse)
def partial_update_author(
    author_id: int,
    author_data: AuthorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    author = author_service.get_author_by_id(db, author_id, current_user=current_user)

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    return author_service.partial_update_author(
        db,
        author,
        author_data
    )


@router.delete("/{author_id}")
def delete_author(
    author_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    author = author_service.get_author_by_id(db, author_id, current_user=current_user)

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    author_service.delete_author(db, author)

    return {
        "message": "Author deleted successfully"
    }