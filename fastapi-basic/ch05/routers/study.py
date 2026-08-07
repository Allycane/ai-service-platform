import pandas as pd
import joblib

from fastapi import APIRouter
from schemas.study_schema import Study

study_router = APIRouter()

# 1. 모델 호출
model = joblib.load('models/model.pkl')

@study_router.post('/predict') # 공부시간을 입력할 경우, 점수를 예측
async def study_predict(features:Study) -> dict:
    # 2. Pydantic -> dict 타입으로 변경
    data = features.model_dump() # {"study_hour" : 3}
    # 모델을 학습시키는데 사용된 입력 데이터가 DataFrame {} 타입이기 떄문에 타입을 변경함

    # 3. dict -> DataFrame 타입으로 변경
    df = pd.DataFrame([data])
    # 단일 항목이기 때문에 []로 묶는다

    # 4. predict 실행 = predict 결과는 리스트(배열) 형태로 반환됨
    prediction = model.predict(df)[0]


    return {
        "predict_score" : round(prediction[0], 2)
    }