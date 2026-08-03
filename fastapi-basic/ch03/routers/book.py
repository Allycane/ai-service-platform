#-------------------------------------------------------------
# 도서 관리 애플리케이션 - CRUD
#-------------------------------------------------------------

from fastapi import APIRouter, HTTPException, status, Path
from schemas.book_schema import book, bookInfo, bookInfos

book_router = APIRouter()

book_list = []

# C
@book_router.post('/book')
async def add_book(bookData: book) -> dict:
    book_list.append(bookData)
    return {
        "message" : "book 정보 추가 완료!"
    }

# R
# All
@book_router.get('/book', response_model=bookInfos)
async def get_bookAll() -> dict:
    return {
        "books" : book_list
    }

# Id
@book_router.get('/book/{id}')
async def get_bookId(id: int) -> dict:
    for book in book_list:
        if book.id == id:
            return {
                "message" : book
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="책의 ID가 존재하지 않음!!!"
    )


# U
@book_router.put('/book/{id}')
async def update_bookId(book_data: bookInfo, id: int = Path(...)) -> dict:
    for book in book_list:
        if book.id == id:
            book.title = book_data.title
            book.price = book_data.price
            book.isbn = book_data.isbn
            return {
                "message" : '책 정보 업데이트 성공',
                "book_data" : book_data
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="책의 ID가 존재하지 않음!!!"
    )
# D
# All
@book_router.delete('/book')
async def delete_bookAll() -> dict:
    if len(book_list) > 0:
        book_list.clear()
        return {
            "message" : "모든 책의 정보를 삭제하였습니다"
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="book_list 내에 책의 정보가 존재하지 않음!!"
    )

# Id
@book_router.delete('/book/{id}')
async def delete_bookId(id:int) -> dict:
    for idx in range(len(book_list)):
        book = book_list[idx]
        if book.id == id:
            book_list.pop(idx)
            return{
                "message" : "책 정보가 삭제되었습니다!"
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="책의 ID가 존재하지 않음!!!"
    )