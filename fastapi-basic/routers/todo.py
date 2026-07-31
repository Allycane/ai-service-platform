# /todo - get(R), post(C), put(U), delete(D)
from fastapi import APIRouter, Path
from pydantic import BaseModel

todo_router = APIRouter()

# Item Model
class Item(BaseModel):
    item:str
    status : str

# Todo Model
class Todo(BaseModel):
    id: int
    item : Item

todo_list = []

# Create
@todo_router.post("/todo")
async def create_todo(todo: Todo) -> dict:
    todo_list.append(todo)
    return {
        "message" : "Create :: Todo"
    }

# Read - ALL
@todo_router.get("/todo/all")
async def read_todo() -> dict:
    return {
        "message::ALL" : todo_list,
    }

# Read
@todo_router.get("/todo")
async def read_todo() -> dict:
    return {
        "message" : "Read :: Todo",
    }

# Read - id별 조회
# POST 내에서 todo : Todo를 지정하고, 값을 입력하는 것이기 때문에
# 데이터를 불러오는 GET 방식 내에서는 todo로 바로 불러오는 것이 가능한 것임
@todo_router.get("/todo/{id}")
async def read_todo(id : int) -> dict:
    for todo in todo_list:
        if todo.id == id:
            return {
                "todo" : todo
            }
    return {
        "message" : "Read :: Todo",
    }

# Update
@todo_router.put("/todo/{id}")
async def update_todo(new_item:Item, id : int = Path(..., title="id")) -> dict:
# PUT은 Body를 통해 넘어오기 때문에 id와 todo_item을 Body에서 찾게된다
# 하지만 Body에서 넘어오는 것은 todo_item 뿐이므로, id를 별도로 명시해주어야 한다
# Path는 클래스, 별도로 import를 진행한다
# PUT 방식은 Body에서 넘어오는 값을 우선으로 하기 때문에 todo_item을 먼저 명시해준다
    for todo in todo_list:
        if todo.id == id:
            todo.item = new_item
            return {
                "message" : "업데이트 성공!!"
            }
    return {
        "message" : "id 확인!!",
    }

# Delete - id별
@todo_router.delete("/todo/{id}")
async def delete_todo(id : int) -> dict:
    for index in range(len(todo_list)): # 딕셔너리 형태의 todo_list의 인덱스를 받아와야 함
        todo = todo_list[index]
        if todo.id == id:
            todo_list.pop(index)
            return {
                "message" : "삭제 성공!!"
            }
            
    return {
        "message" : "id 확인!!"
    }

# Delete - 전체삭제
@todo_router.delete("/todo")
async def delete_todo(id : int) -> dict:
    if len(todo_list) > 0:
        todo_list.clear()
        return { "message" : "전체 삭제 성공!!"}
            
    return {
        "message" : "todo_list 데이터가 존재하지 않습니다"
    }