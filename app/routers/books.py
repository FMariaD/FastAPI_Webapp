from typing import List

from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException
from models.api_models import Book, BookCreate, BookUpdate
from models.db_models import Book as DBBook
from sqlalchemy.orm import Session

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=List[Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve a list of books with pagination support.

    Args:
        skip (int): Number of records to skip (for pagination).
        limit (int): Maximum number of records to return.
        db (Session): Database session.

    Returns:
        List[Book]: List of book objects.
    """
    books = db.query(DBBook).offset(skip).limit(limit).all()
    return books


@router.post("/", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """Create a new book record.

    Args:
        book (BookCreate): Book data to create.
        db (Session): Database session.

    Returns:
        Book: The newly created book object.
    """
    db_book = DBBook(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get("/{book_id}", response_model=Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """Retrieve a single book by its ID.

    Args:
        book_id (int): ID of the book to retrieve.
        db (Session): Database session.

    Returns:
        Book: The requested book object.

    Raises:
        HTTPException: 404 if book is not found.
    """
    book = db.query(DBBook).filter(DBBook.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=Book)
def update_book(
    book_id: int,
    book: BookUpdate,
    db: Session = Depends(get_db),
):
    """Update an existing book record.

    Args:
        book_id (int): ID of the book to update.
        book (BookUpdate): New book data (partial updates supported).
        db (Session): Database session.

    Returns:
        Book: The updated book object.

    Raises:
        HTTPException: 404 if book is not found.
    """
    db_book = db.query(DBBook).filter(DBBook.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = book.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)

    db.commit()
    db.refresh(db_book)
    return db_book


@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
):
    """Delete a book record.

    Args:
        book_id (int): ID of the book to delete.
        db (Session): Database session.

    Returns:
        dict: Success message.

    Raises:
        HTTPException: 404 if book is not found.
    """
    book = db.query(DBBook).filter(DBBook.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    return {"message": "Книга успешно удалена"}
