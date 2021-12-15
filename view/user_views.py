import bcrypt, requests

from typing import Optional

from fastapi           import APIRouter, Depends, Response, Request
from fastapi.responses import JSONResponse, RedirectResponse

from sqlalchemy.orm import Session

from service import user_service
from model   import crud, schemas, database
from env     import rest_api_key


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

# 카카오 인가 코드 받기
@router.get('/login/kakao', tags=['카카오로그인'])
def kakao():
    REST_API_KEY = rest_api_key
    REDIRECT_URI = 'http://localhost:8000/users/login/kakao/callback'
    url          = f'https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}'
    return RedirectResponse(url)

# 카카오 토큰 받기
@router.get('/login/kakao/callback', tags=['카카오로그인'])
async def kakaoAuth(token_response: Response, code: Optional[str]="NONE"):
    REST_API_KEY = rest_api_key
    REDIRECT_URI = 'http://localhost:8000/users/login/kakao/callback'
    url          = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&code={code}'
    response     = requests.post(url)
    result       = response.json()
    token_response.set_cookie(key='kakao', value=str(result['access_token']))
    return {'code': result}

# 카카오 로그아웃
@router.get('/kakaologout', tags=['카카오 로그아웃'])
def kakaoLogout(request: Request, token_response: Response):
    url      = 'https://kapi.kakao.com/v1/user/unlink'
    TOKEN    = request.cookies['kakao']
    header   = {'Authorization': f'Bearer {TOKEN}'}
    response = requests.post(url, headers=header)
    result   = response.json()
    token_response.set_cookie(key='kakao', value=None)
    return {'logout': result}


