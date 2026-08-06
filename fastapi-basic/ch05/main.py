from fastapi import FastAPI
from routers.study import study_router

app = FastAPI()

# 모델 연동
app.include_router(study_router)