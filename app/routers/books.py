from typing import List

from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException
from models.api_models import Book, BookCreate
from models.db_models import Book as DBBook
from sqlalchemy.orm import Session

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=List[Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = db.query(DBBook).offset(skip).limit(limit).all()
    return books


@router.post("/", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = DBBook(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get("/{book_id}", response_model=Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(DBBook).filter(DBBook.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
