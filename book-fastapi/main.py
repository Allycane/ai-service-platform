from fastapi import FastAPI
from routers.book import router

# DB 연동
from database import Base, engine

# 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(router, prefix='/fastapi')