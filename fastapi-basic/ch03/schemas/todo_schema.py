from typing import List
from pydantic import BaseModel, ConfigDict, Field

# TodoItem Model -> 요청 시 호출되는 모델 객체
class TodoItem(BaseModel):
    item : str
    model_config = ConfigDict(
        json_schema_extra={
            "examples" : [
                {"item" : "수정할 아이템 입력"}
            ]
        }
    )

# TodoItems Model -> 전체 리스트 호출 시 출력
class TodoItems(BaseModel):
    todos : List[TodoItem] = Field(default_factory=list)

# Todo Model
class Todo(BaseModel):
    id:int
    item:str

    model_config = ConfigDict( # swagger 테스트 시 샘플 실행
        json_schema_extra={
            "examples" : [
                {
                    "id" : 1,
                    "item" : "FastAPI 공부하기"
                }
            ]
        }
    )
