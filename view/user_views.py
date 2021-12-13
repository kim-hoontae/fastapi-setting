import bcrypt

from fastapi           import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from service import user_service
from model   import crud, schemas, database


router = APIRouter(prefix = '/users')

@router.post('/signup', response_model=schemas.User, tags=['회원가입'])
def signup(user: schemas.Signup, db: Session = Depends(database.get_db)):
    user_db = crud.get_user_by_email(db, email=user.email)
    # 유저의 이메일이 있을 경우 예외 처리
    if user_db:
        return JSONResponse(content={'MESSAGE':'INVALID_EMAIL'}, status_code=400)
    
    # 비밀번호 정규식 특수문자 숫자포함 8자리 이상
    if not user_service.password_validation(user.password):
        return JSONResponse(content={'MESSAGE':'NOT_PASSWORD_FOMAT'}, status_code=400)

    return crud.create_user(db=db, user=user)


@router.post('/login',response_model=schemas.Token, tags=['로그인'])
def login(user: schemas.Login, db: Session = Depends(database.get_db)):
    user_db  = crud.get_user_by_email(db, email=user.email)
    # 유저 email 확인
    if not user_db :
        return JSONResponse(content={'MESSAGE':'INVALID_EMAIL'}, status_code=400)

    password = bcrypt.checkpw(user.password.encode('utf-8'), user_db.password.encode('utf-8'))    
    # 유저 password 확인
    if not password:
        return JSONResponse(content={'MESSAGE':'INVALID_PASSWORD'}, status_code=400)
    
    access_token = user_service.access_token(user_db)
    
    return JSONResponse(content={'MESSAGE':'SUCCESS', 'TOKEN':access_token}, status_code=200)
