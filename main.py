from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from exceptions import (
    AlreadyExistsException,
    NotFoundException,
    ValidationException,
)

from routers.author import router as author_router
from routers.category import router as category_router
from routers.book import router as book_router
from routers.auth import router as auth_router
from routers.borrow import router as borrow_router
from routers.dashboard import router as dashboard_router


app = FastAPI(
    title="Library Management System",
    version="1.0.0"
)


@app.exception_handler(NotFoundException)
async def not_found_exception_handler(
    request: Request,
    exc: NotFoundException,
):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": str(exc),
        },
    )


@app.exception_handler(AlreadyExistsException)
async def already_exists_exception_handler(
    request: Request,
    exc: AlreadyExistsException,
):
    return JSONResponse(
        status_code=409,
        content={
            "success": False,
            "message": str(exc),
        },
    )


@app.exception_handler(ValidationException)
async def validation_exception_handler(
    request: Request,
    exc: ValidationException,
):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": str(exc),
        },
    )


app.include_router(auth_router)
app.include_router(author_router)
app.include_router(category_router)
app.include_router(book_router)
app.include_router(borrow_router)
app.include_router(dashboard_router)