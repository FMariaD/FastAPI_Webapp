from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# for books
class BookBase(BaseModel):
    """Base model for book data containing common fields."""

    title: str
    author: str
    year: Optional[int] = None
    description: Optional[str] = None


class BookCreate(BookBase):
    """Model for creating new books (inherits all BookBase fields)."""

    pass


class BookUpdate(BookBase):
    """Model for updating existing books (inherits all BookBase fields)."""

    pass


class Book(BookBase):
    """Complete book model including database ID and calculated rating."""

    id: int
    average_rating: Optional[float] = None

    class Config:
        from_attributes = True


# ///


# for users and books
class UserBookBase(BaseModel):
    """Base model for user-book relationships with status and rating."""

    status: str = Field(..., pattern="^(read|planned)$")
    rating: Optional[int] = Field(None, ge=1, le=5)


class UserBookCreate(UserBookBase):
    """Model for creating new user-book relationships."""

    book_id: int


class UserBook(UserBookBase):
    """Complete user-book relationship model with database IDs."""

    id: int
    user_id: int
    book_id: int

    class Config:
        from_attributes = True


class UserBookUpdate(UserBookBase):
    """Model for updating existing user-book relationships."""

    pass


# ///

# for auth


class Token(BaseModel):
    """Authentication token response model."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Model for decoded token payload data."""

    username: str | None = None


class UserCreate(BaseModel):
    """Model for user registration data."""

    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """Model for user login credentials."""

    username: str
    password: str


# ///
