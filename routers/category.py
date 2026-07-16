from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
)
from services import category as category_service

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.post("/", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
):
    new_category = category_service.create_category(
        db,
        category,
    )

    if new_category is None:
        raise HTTPException(
            status_code=409,
            detail="Category already exists",
        )

    return new_category


@router.get("/", response_model=list[CategoryResponse])
def get_categories(
    db: Session = Depends(get_db),
):
    return category_service.get_all_categories(db)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    category = category_service.get_category_by_id(
        db,
        category_id,
    )

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
):
    category = category_service.get_category_by_id(
        db,
        category_id,
    )

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return category_service.update_category(
        db,
        category,
        category_data,
    )


@router.patch("/{category_id}", response_model=CategoryResponse)
def partial_update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
):
    category = category_service.get_category_by_id(
        db,
        category_id,
    )

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return category_service.partial_update_category(
        db,
        category,
        category_data,
    )


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    category = category_service.get_category_by_id(
        db,
        category_id,
    )

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    category_service.delete_category(
        db,
        category,
    )

    return {
        "message": "Category deleted successfully"
    }