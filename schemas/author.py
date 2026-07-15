from datetime import date
from pydantic import BaseModel, ConfigDict

class AuthorCreate(BaseModel):
    full_name: str
    bio: str | None = None
    date_of_birth: date | None = None


class AuthorResponse(BaseModel):
    id: int
    full_name: str
    bio: str | None
    date_of_birth: date | None
    photo: str | None

    model_config = ConfigDict(from_attributes=True)


class AuthorUpdate(BaseModel):
    full_name: str
    bio: str | None = None
    date_of_birth: date | None = None
