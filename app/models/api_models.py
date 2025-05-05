from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# for books
class BookBase(BaseModel):
    title: str
    author: str
    year: Optional[int] = None
    description: Optional[str] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class Book(BookBase):
    id: int
    average_rating: Optional[float] = None

    class Config:
        from_attributes = True


# ///


# for users and books
class UserBookBase(BaseModel):
    status: str = Field(..., pattern="^(read|planned)$")
    rating: Optional[int] = Field(None, ge=1, le=5)


class UserBookCreate(UserBookBase):
    book_id: int


class UserBook(UserBookBase):
    id: int
    user_id: int
    book_id: int

    class Config:
        from_attributes = True


class UserBookUpdate(UserBookBase):
    pass


# ///

# for auth


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


# ///
