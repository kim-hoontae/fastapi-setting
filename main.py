import uvicorn

from fastapi                 import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from model.database import engine
from model          import models
from view           import user_views

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
    app.include_router(user_views.router)


    # 미들웨어 정의
    origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000"
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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)