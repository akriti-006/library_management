from fastapi import FastAPI
from routers.author import router as author_router
from routers.category import router as category_router
from routers.book import router as book_router

app = FastAPI(
    title="Library Management System",
    version="1.0.0"
)

app.include_router(author_router)
app.include_router(category_router)
app.include_router(book_router)
