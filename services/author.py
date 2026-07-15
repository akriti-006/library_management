from sqlalchemy.orm import Session

from models.author import Author
from schemas.author import AuthorCreate, AuthorUpdate


def create_author(
    db: Session,
    author_data: AuthorCreate
):
    author = Author(
        full_name=author_data.full_name,
        bio=author_data.bio,
        date_of_birth=author_data.date_of_birth,
    )

    db.add(author)
    db.commit()
    db.refresh(author)

    return author


def get_all_authors(db: Session):
    return db.query(Author).all()


def get_author_by_id(
    db: Session,
    author_id: int
):
    return (
        db.query(Author)
        .filter(Author.id == author_id)
        .first()
    )


def update_author(
    db: Session,
    author: Author,
    author_data: AuthorUpdate
):
    author.full_name = author_data.full_name
    author.bio = author_data.bio
    author.date_of_birth = author_data.date_of_birth

    db.commit()
    db.refresh(author)

    return author


def partial_update_author(
    db: Session,
    author: Author,
    author_data: AuthorUpdate
):
    update_data = author_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(author, key, value)

    db.commit()
    db.refresh(author)

    return author


def delete_author(
    db: Session,
    author: Author
):
    db.delete(author)
    db.commit()