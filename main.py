from fastapi import FastAPI, HTTPException
import mysql.connector
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# MySQL 데이터베이스 연결 설정
DB_HOST = "localhost"
DB_USER = "user"
DB_PASSWORD = ""
DB_NAME = "stock_db"

# 데이터베이스 연결 함수
def connect_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# 최근 예측값 모델
class Prediction(BaseModel):
    date: datetime
    prediction: float

# 최근 예측값 가져오는 API 엔드포인트
@app.get("/latest_prediction", response_model=Prediction)
def get_latest_prediction():
    db = connect_db()
    cursor = db.cursor()

    # 최신 예측값을 가져오는 쿼리
    query = "SELECT date, prediction FROM predictions ORDER BY date DESC LIMIT 1"
    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    db.close()

    # 예측값이 없을 때 기본 응답 설정
    if result is None:
        raise HTTPException(status_code=404, detail="No prediction data available")

    latest_prediction = {
        "date": result[0],
        "prediction": result[1]
    }

    return latest_prediction

