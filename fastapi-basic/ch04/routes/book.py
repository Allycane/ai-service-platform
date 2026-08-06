from fastapi import APIRouter, Depends, HTTPException, status, Path
from schemas.book_schema import Book, Book_Item, Books
from database import get_db
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from models.book_model import BookModel


book_router = APIRouter()


# C: Insert
@book_router.post("/book")
async def add_book(book_data : Book_Item, db:Session = Depends(get_db)) -> dict:
    bookModel = BookModel(
        title = book_data.title,
        price = book_data.price,
        isbn = book_data.isbn
    )

    # 모델에 데이터 추가
    db.add(bookModel) # SQL 생성 -> Insert into "books" values(?, ?, ?)
    # db 전송 및 실행
    db.commit()
    # 실행 결과 받기 - Book 타입으로 받기 (title, price, isbn)
    db.refresh(bookModel)


    return {
        "message" : "등록 성공!!",
        "book" :  {
                    "id" : bookModel.id,
                    'title' : bookModel.title,
                    'price' : bookModel.price,
                    'isbn' : bookModel.isbn
                }
    }

# R : Select All
@book_router.get('/books', response_model=Books) # [{Book_Item}, {Book_Item}]
async def get_all(db:Session = Depends(get_db)):
    # DB연동 로직
    # execute는 한번에 실행시킨다
    book_list = db.execute(
        select(BookModel).order_by(BookModel.id)
    ) # [{}, {}, ...]

    result = book_list.scalars().all()

    return {
        "books" : result
    }

# R : Select Id
@book_router.get('/book/{id}', response_model=Book)
async def get_id(id:int, db:Session = Depends(get_db)) -> dict:
    # DB에 변형을 주는 것이 아니기 때문에 db.get() 함수만 진행함
    # Select 쿼리 생성, 실행 <-- DB
    book = db.get(BookModel, id)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ID does not exist!!!"
        )

    return book

# U : Update
@book_router.put('/book/{id}', response_model=Book)
async def update_id(new_data:Book_Item, id:int=Path(...), db:Session=Depends(get_db)) -> dict:

    # 1. get()를 사용하여 DB의 데이터를 불러온다
    book = db.get(BookModel, id)

    # 1-1. 입력받은 id가 DB에 존재하지 않을 경우
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ID does not exist!!!"
        )
    
    # 2. 데이터 변경
    book.title = new_data.title
    book.price = new_data.price
    book.isbn = new_data.isbn

    # 3. DB에 반영
    db.commit()

    # 4. DB 갱신
    db.refresh(book)

    return book

# D : Delete all
@book_router.delete('/books')
async def delete_all(db:Session=Depends(get_db)) -> dict:
    result = db.execute(delete(BookModel))
    db.commit()

    if result.rowcount == 0:
        return {
            "message" : "삭제할 데이터가 존재하지 않습니다!!!"
        }

    return{
        "message" : "전체 데이터 삭제가 완료되었습니다~!!"
    }

# D : Delete Id
@book_router.delete('/book/{id}')
async def delete_id(id:int, db:Session=Depends(get_db)) -> dict:
    # 1. DB 상 id를 입력하여 해당 데이터 불러오기
    book = db.get(BookModel, id)

    # 1-1. id가 존재하지 않을 경우
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ID does not exitst!!!"
        )

    # 2. 데이터 삭제
    db.delete(book)

    # 3. DB에 반영
    db.commit()

    # 가져올 데이터가 존재하지 않으므로 refresh()는 진행하지 않음

    return {
        "message" : "도서 데이터 삭제 완료~!!"
    }