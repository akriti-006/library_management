from fastapi import FastAPI
from routers.author import router as author_router

app = FastAPI(
    title="Library Management System",
    version="1.0.0"
)

app.include_router(author_router)


# @app.get("/")
# def home():
#     return {
#         "message": "Welcome to Library Management System"
#     }