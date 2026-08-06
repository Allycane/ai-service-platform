from pydantic import BaseModel, ConfigDict, Field
from typing import List

# post 메소드 호출시 매핑되는 모델
class Book_Item(BaseModel):
    title: str
    price: int
    isbn: int

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "FastAPI",
                    "price": 20000,
                    "isbn": 1234
                }
            ]
        }
    )

class Book(BaseModel):
    id: int
    title: str
    price: int
    isbn: int

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "title": "FastAPI",
                    "price": 20000,
                    "isbn": 1234
                }
            ]
        }
    )

# Books 클래스 정의
class Books(BaseModel):
    books : List[Book] = Field(default_factory=list)