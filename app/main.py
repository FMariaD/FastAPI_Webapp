from db.init_db import init_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

init_db()

app = FastAPI(
    title="Сервис для оценки и поиска книг",
    description="Основано на фреймворке FastAPI.",
    version="0.0.1",
    contact={
        "name": "Федорова Мария",
        "url": "https://github.com/FMariaD/FastAPI_Webapp",
        "email": "fedorova.md@phystech.edu",
    },
)

origins = ["https://localhost:8087", "http://localhost:8087", "localhost:8087", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Это проект для курса Программирование на Python (2 семестр)"}


# app.include_router(router)
