from core.security import get_password_hash
from db.session import Base, engine
from models.db_models import Book, User, UserBook
from sqlalchemy import text
from sqlalchemy.orm import Session


def init_db():
    """Initializes db and fills it with default values"""
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        if session.query(Book).count() > 0:
            return

        # sample users
        users = [
            User(
                username="user",
                email="user@example.com",
                hashed_password=get_password_hash("password"),
            ),
            User(
                username="admin",
                email="admin@example.com",
                hashed_password=get_password_hash("password123"),
            ),
        ]
        session.add_all(users)
        session.commit()

        # sample books
        books = [
            Book(
                title="Великий Гэтсби",
                author="Фрэнсис Скотт Фицджеральд",
                year=1925,
                description="Книга 1",
            ),
            Book(
                title="Убить пересмешника",
                author="Харпер Ли",
                year=1960,
                description="Книга 2",
            ),
            Book(
                title="1984",
                author="Джордж Оруэлл",
                year=1949,
                description="Длинное описание книги 3",
            ),
            Book(
                title="Гордость и предубеждение",
                author="Джейн Остин",
                year=1813,
                description="Книга 4",
            ),
            Book(
                title="Хоббит",
                author="Дж. Р. Р. Толкин",
                year=1937,
                description="Книга 5",
            ),
        ]
        session.add_all(books)
        session.commit()

        # sample read&planned books
        user_books = [
            UserBook(user_id=1, book_id=1, status="read", rating=3),
            UserBook(user_id=1, book_id=2, status="read", rating=4),
            UserBook(user_id=1, book_id=3, status="planned", rating=None),
            UserBook(user_id=1, book_id=5, status="read", rating=5),
            UserBook(user_id=2, book_id=1, status="read", rating=4),
            UserBook(user_id=2, book_id=4, status="read", rating=2),
            UserBook(user_id=2, book_id=2, status="planned", rating=None),
            UserBook(user_id=2, book_id=5, status="read", rating=5),
        ]
        session.add_all(user_books)
        session.commit()

        session.execute(
            text("""
        CREATE INDEX IF NOT EXISTS idx_user_books_user_id ON user_books (user_id);
        """)
        )
        session.execute(
            text("""
        CREATE INDEX IF NOT EXISTS idx_user_books_book_id ON user_books (book_id);
        """)
        )
        session.execute(
            text("""
        CREATE INDEX IF NOT EXISTS idx_user_books_status ON user_books (status);
        """)
        )
