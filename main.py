import uvicorn
from dataclasses             import asdict
from typing                  import Optional
from fastapi                 import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from model          import models
from model.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

# 타이틀 제목 설정
description = """
# FastAPI-Setting
"""

def create_app():
    """
    앱 함수 실행
    :return:
    """
    app = FastAPI(title='FastAPI-Setting', description=description)
    # 라우터 정의

    # 미들웨어 정의
    origins = [
        "http://localhost.tiangolo.com",
        "https://localhost.tiangolo.com",
        "http://localhost",
        "http://localhost:8080",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

app = create_app()