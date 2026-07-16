from slugify import slugify
from sqlalchemy.orm import Session

from models.category import Category
from schemas.category import CategoryCreate, CategoryUpdate


def create_category(
    db: Session,
    category_data: CategoryCreate
):
    existing_category = get_category_by_name(
        db,
        category_data.name
    )

    if existing_category:
        return None

    category = Category(
        name=category_data.name,
        slug=slugify(category_data.name),
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def get_all_categories(db: Session):
    return db.query(Category).all()


def get_category_by_id(
    db: Session,
    category_id: int
):
    return (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )


def get_categories_by_ids(
    db: Session,
    category_ids: list[int]
):
    return (
        db.query(Category)
        .filter(Category.id.in_(category_ids))
        .all()
    )


def update_category(
    db: Session,
    category: Category,
    category_data: CategoryUpdate
):
    category.name = category_data.name
    category.slug = slugify(category_data.name)

    db.commit()
    db.refresh(category)

    return category


def partial_update_category(
    db: Session,
    category: Category,
    category_data: CategoryUpdate
):
    update_data = category_data.model_dump(exclude_unset=True)

    if "name" in update_data:
        update_data["slug"] = slugify(update_data["name"])

    for key, value in update_data.items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)

    return category


def delete_category(
    db: Session,
    category: Category
):
    db.delete(category)
    db.commit()


def get_category_by_name(
    db: Session,
    name: str
):
    return (
        db.query(Category)
        .filter(Category.name == name)
        .first()
    )