from pydantic import BaseModel, ConfigDict, Field
from typing import List

class Book(BaseModel):
    id : int
    title : str
    author : str
    publisher : str
    year : str
    status : str

# Insert 혹은 Update를 위한 모델
class BookItem(BaseModel):
    title : str
    author : str
    publisher : str
    year : str
    status : str

# DB에 입력하기 위해서는 str이 아닌 String 타입으로 넘겨야 함

    model_config = ConfigDict(
        json_schema_extra={
            "examples" : [
                {
                    "title" : "FastAPI 정복!",
                    "author" : "홍길동",
                    "publisher" : "파이썬 출판사",
                    "year" : "2026",
                    "status" : "대여가능"
                }
            ]
        }
    )


class BookItems(BaseModel):
    books:List[Book] = Field(default_factory=list)