from pydantic import BaseModel, ConfigDict, Field
from typing import List

class bookInfo(BaseModel):
    title : str
    price : int
    isbn : int

    model_config = ConfigDict(
        json_schema_extra= {
            "examples" : [
                {
                    "title" : "용의자 X",
                    "price" : 20000,
                    "isbn" : 1234
                }
            ]
        }
    )

class bookInfos(BaseModel):
    books : List[bookInfo] = Field(default_factory=list)

# post 메소드 호출 시 매핑되는 모델
class book(BaseModel):
    id : int
    title : str
    price : int
    isbn : int

    model_config = ConfigDict(
        json_schema_extra={
            "examples" : [
                {
                    "id" : 1,
                    "title" : "용의자 X",
                    "price" : 20000,
                    "isbn" : 1234
                }
            ]
        }
    )