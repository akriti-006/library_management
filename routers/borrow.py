from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user
from models.user import User
from schemas.borrow import (
    BorrowCreate,
    BorrowResponse,
    ReturnBookResponse,
)
from services.borrow import borrow_book, return_book, get_my_borrowed_books, get_borrow_history

router = APIRouter(
    prefix="/borrow",
    tags=["Borrow Records"],
)


@router.post("/", response_model=BorrowResponse)
def borrow(borrow_data: BorrowCreate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return borrow_book(
        db=db,
        current_user=current_user,
        book_id=borrow_data.book_id,
    )


@router.put("/return/{borrow_id}", response_model=ReturnBookResponse)
def return_borrowed_book(borrow_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return return_book(
        db=db,
        borrow_id=borrow_id,
        current_user=current_user
    )


@router.get("/my-books", response_model=list[BorrowResponse])
def my_books(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_my_borrowed_books(
        db=db,
        current_user=current_user,
    )


@router.get("/history", response_model=list[BorrowResponse])
def borrow_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_borrow_history(
        db=db,
        current_user=current_user,
    )
