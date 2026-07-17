from datetime import date

from pydantic import BaseModel, ConfigDict


class BorrowCreate(BaseModel):
    book_id: int


class BorrowResponse(BaseModel):
    id: int
    book_id: int
    member_id: int
    borrowed_on: date
    due_date: date
    returned_on: date | None
    is_returned: bool

    model_config = ConfigDict(
        from_attributes=True
    )


class ReturnBookResponse(BaseModel):
    message: str
    borrow_record: BorrowResponse
    late_days: int
    fine_amount: int