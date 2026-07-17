from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_books: int
    available_books: int
    borrowed_books: int
    total_members: int
    active_borrow_records: int
    returned_books: int
    total_authors: int
    total_categories: int
