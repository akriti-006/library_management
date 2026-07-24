from pydantic import BaseModel


class TopBorrowedBookResponse(BaseModel):
    title: str
    borrow_count: int


class DashboardResponse(BaseModel):
    total_books: int
    available_books: int
    borrowed_books: int
    total_members: int
    active_borrow_records: int
    returned_books: int
    overdue_borrows: int
    total_authors: int
    total_categories: int
    top_borrowed_books: list[TopBorrowedBookResponse]