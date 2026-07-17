from sqlalchemy.orm import Session

from models.user import User
from schemas.auth import UserRegister
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_access_token,
)
from exceptions import (
    AlreadyExistsException,
    NotFoundException,
    ValidationException,
)



def register_user(
    db: Session,
    user_data: UserRegister,
):
    # Check username
    existing_username = (
        db.query(User)
        .filter(User.username == user_data.username)
        .first()
    )

    if existing_username:
        raise AlreadyExistsException(
            "Username already exists."
        )

    # Check email
    existing_email = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_email:
        raise AlreadyExistsException(
            "Email already exists."
        )

    # Create user
    user = User(
        username=user_data.username,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        hashed_password=hash_password(
            user_data.password
        ),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def login_user(
    db: Session,
    email: str,
    password: str,
):
    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if user is None:
        raise NotFoundException(
            "User not found."
        )

    if not user.is_active:
        raise ValidationException(
            "User account is inactive."
        )

    if not verify_password(
        password,
        user.hashed_password,
    ):
        raise ValidationException(
            "Invalid credentials."
        )

    access_token = create_access_token(
    {"sub": str(user.id)}
)

    refresh_token = create_refresh_token(
        {"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user,
    }


def get_current_user(
    db: Session,
    user_id: int,
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise NotFoundException(
            "User not found."
        )

    return user


def refresh_access_token(refresh_token: str):
    payload = verify_access_token(refresh_token)

    if payload is None:
        raise ValidationException(
            "Invalid refresh token."
        )

    user_id = payload.get("sub")

    access_token = create_access_token(
        {"sub": user_id}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }