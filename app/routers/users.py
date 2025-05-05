from typing import List

from core.security import get_current_user
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException
from models.api_models import UserBook, UserBookCreate, UserBookUpdate
from models.db_models import User
from models.db_models import UserBook as DBUserBook
from sqlalchemy.orm import Session

router = APIRouter(prefix="/account", tags=["users"])


@router.get("/books", response_model=List[UserBook])
def get_my_books(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return db.query(DBUserBook).filter(DBUserBook.user_id == current_user.id).all()


@router.post("/books", response_model=UserBook)
def add_book_to_my_list(
    book_data: UserBookCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_book = DBUserBook(
        user_id=current_user.id,
        book_id=book_data.book_id,
        status=book_data.status,
        rating=book_data.rating,
    )
    db.add(user_book)
    db.commit()
    db.refresh(user_book)
    return user_book


@router.put("/books/{book_id}", response_model=UserBook)
def update_book_in_my_list(
    book_id: int,
    book_data: UserBookUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_book = (
        db.query(DBUserBook)
        .filter(DBUserBook.user_id == current_user.id, DBUserBook.book_id == book_id)
        .first()
    )

    if not user_book:
        raise HTTPException(status_code=404, detail="Book not found in user's list")

    update_data = book_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user_book, field, value)

    db.commit()
    db.refresh(user_book)
    return user_book


@router.delete("/books/{book_id}")
def remove_book_from_my_list(
    book_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_book = (
        db.query(DBUserBook)
        .filter(DBUserBook.user_id == current_user.id, DBUserBook.book_id == book_id)
        .first()
    )

    if not user_book:
        raise HTTPException(status_code=404, detail="Book not found in user's list")

    db.delete(user_book)
    db.commit()
    return {"message": "Книга успешно удалена из списка"}
