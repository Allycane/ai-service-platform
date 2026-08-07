from fastapi import APIRouter, Depends, HTTPException, status, Path
from schemas.book_schema import Book, BookItem, BookItems
from models.book_model import BookModel
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()

# MiddleWare (CORS)

books = []

# C : Insert
@router.post('/book')
async def add_book(bookItem:BookItem, db:Session=Depends(get_db)) -> dict:
    # 1. BookModel 생성 및 입력 데이터 추가
    bookModel = BookModel(
        title = bookItem.title,
        author = bookItem.author,
        publisher = bookItem.publisher,
        year = bookItem.year,
        status = bookItem.status
    )
    # 2. db.add() - SQL 생성
    db.add(bookModel)
    # 3. db.commit() - Transaction 실행
    db.commit()
    # 4. db.refresh(ModelType) - 실행 결과 가져오기
    db.refresh(bookModel)

    return {
        "message" : "등록 성공!",
        "book" : {
            "id" : bookModel.id,
            "title" : bookModel.title,
            "author" : bookModel.author,
            "publisher" : bookModel.publisher,
            "year" : bookModel.year,
            "status" : bookModel.status
        }
    }

# R
@router.get('/books', response_model=BookItems)
async def getAll(db:Session=Depends(get_db)) -> list:
    init_books = db.execute(
        select(BookModel).order_by(BookModel.id)
    )
    books = init_books.scalars().all() # [{}, {}, ...]


    return {
        "books" : books
    }

# U
@router.put('/book/{id}')
async def updateId(bookItem:BookItem, id:int = Path(...), db:Session=Depends(get_db)) -> dict:
    book = db.get(BookModel, id)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ID does not exist!!"
        )

    book.title = bookItem.title
    book.author = bookItem.author
    book.publisher = bookItem.publisher
    book.year = bookItem.year
    book.status = bookItem.status

    db.commit()

    return {
        "isUpdate" : True
    }


# D - Delete ID
@router.delete('/book/{id}')
async def deleteId(id:int, db:Session=Depends(get_db)):
    book = db.get(BookModel, id)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ID does not exist!!"
        )

    db.delete(book)
    db.commit()

    return {
        "isDelete" : True
    }