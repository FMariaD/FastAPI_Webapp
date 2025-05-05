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
    """Retrieve all books in the current user's collection.

    Args:
        current_user (User): Authenticated user (from JWT token).
        db (Session): Database session.

    Returns:
        List[UserBook]: All books associated with the user.
    """
    return db.query(DBUserBook).filter(DBUserBook.user_id == current_user.id).all()


@router.post("/books", response_model=UserBook)
def add_book_to_my_list(
    book_data: UserBookCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Add a new book to the user's collection.

    Args:
        book_data (UserBookCreate): Book data including book_id, status and optional rating.
        current_user (User): Authenticated user (from JWT token).
        db (Session): Database session.

    Returns:
        UserBook: The newly created user-book relationship.

    Raises:
        HTTPException: 400 if book already exists in user's list.
    """
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
    """Update a book's status or rating in the user's collection.

    Args:
        book_id (int): ID of the book to update.
        book_data (UserBookUpdate): New status/rating values.
        current_user (User): Authenticated user (from JWT token).
        db (Session): Database session.

    Returns:
        UserBook: Updated book record.

    Raises:
        HTTPException: 404 if book not found in user's collection.
    """
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
    """Remove a book from the user's collection.

    Args:
        book_id (int): ID of the book to remove.
        current_user (User): Authenticated user (from JWT token).
        db (Session): Database session.

    Returns:
        dict: Success message with confirmation.

    Raises:
        HTTPException: 404 if book not found in user's collection.
    """
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
