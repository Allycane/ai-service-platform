from fastapi import APIRouter, Path, HTTPException, status
from schemas.todo_schema import Todo, TodoItem, TodoItems

todo_router = APIRouter()

# todo_list
todo_list = []


# CRUD

# C
@todo_router.post('/todo')
async def add_todo(todo : Todo) -> dict:
    todo_list.append(todo)
    return {
        "message" : "Todo 객체 추가완료"
    }

# R
@todo_router.get('/todo', response_model=TodoItems)
async def getAll() -> dict:
    return {
        "todos" : todo_list
    }

@todo_router.get('/todo/{id}')
async def getId(id:int) -> dict:
    for todo in todo_list:
        if todo.id == id:
            return {
                "message" : todo
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="ID가 존재하지 않음!!!",
    )
    # return {
    #     "message" : "ID가 존재하지 않음!!!"
    # }

# U
@todo_router.put('/todo/{id}')
async def update_todo(todo_data:TodoItem, id: int = Path(...)) -> dict:
    for todo in todo_list:
        if todo.id == id:
            todo.item = todo_data.item
            return {
                "message" : "todo 업데이트 성공"
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="ID가 존재하지 않음!!!",
     )
    # return {
    #     "message" : "ID가 존재하지 않음!!!"
    # }

# D
# ALL
@todo_router.delete('/todo')
async def deleteAll() -> dict:
    if len(todo_list) > 0:
        todo_list.clear()
        return{
            "message" : "todo_list 삭제 성공"
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="todo_list가 존재하지 않음!!!",
     )
    # return {
    #     "message" : "todo_list 데이터가 존재하지 않음!!!!"
    # }

# ID
@todo_router.delete('/todo/{id}')
async def deleteId(id: int) -> dict:
    for idx in range(len(todo_list)):
        todo = todo_list[idx]
        if todo.id == id:
            todo_list.pop(idx)
            return {
                "message" : "todo 삭제 완료"
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="ID가 존재하지 않음!!!",
     )
    # return {
    #     "message" : "ID가 존재하지 않음!!!"
    # }