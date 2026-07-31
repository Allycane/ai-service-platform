from fastapi import FastAPI
# 라우팅 대상 파일 임포트
from routers.hello import hello_router
from routers.todo import todo_router

app = FastAPI() # FastAPI 서버 생성

@app.get("/") # http://127.0.0.1:8000/
async def welcome() -> dict: # arrow function { key:value }
    return{
        "message" : "GET :: welcome to FastAPI world!!",
    }

@app.post("/") # http://127.0.0.1:8000/
async def welcome() -> dict: # arrow function { key:value }
    return{
        "message" : "POST :: welcome to FastAPI world!!",
    }

# Code Include
app.include_router(hello_router)
app.include_router(todo_router)