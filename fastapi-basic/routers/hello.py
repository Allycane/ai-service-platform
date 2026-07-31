from fastapi import APIRouter
from pydantic import BaseModel

hello_router = APIRouter()

# Person 클래스 정의
class Person(BaseModel):
    name: str
    age: int
# BaseModel을 parameter로 받아야 request, response할 때 왔다갔다 할 수 있음

person_list = []

# Path Variable (경로 매개변수) - GET 방식
@hello_router.get("/hello/{name}") # http://127.0.0.1:8000/hello/hong
async def say_hello(name: str) -> dict: # arrow function { key:value }
    return{
        "message" : "Hello World!!" + name,
    }

# QueryString (쿼리 매개변수) - GET 방식
@hello_router.get("/hello2") # http://127.0.0.1:8000/hello?name=hong
async def say_hello(name: str) -> dict: # arrow function { key:value }
    return{
        "message" : "Hello World!!" + name
    }

@hello_router.post("/hello") # http://127.0.0.1:8000/
async def say_hello(person: Person) -> dict: # arrow function { key:value }
    person_list.append(person)
    return{
        "message" : person
    }