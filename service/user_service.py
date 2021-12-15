import re, jwt

from requests.models import Response

from datetime import datetime, timedelta
from typing import Optional

from model import schemas
from env import SECRET_KEY, ALGORITHM

def password_validation(password: str):
    if re.search(r'^(?=(.*[A-Za-z]))(?=(.*[0-9]))(?=(.*[@#$%^!&+=.\-_*]))([a-zA-Z0-9@#$%^!&+=*.\-_]){8,}$', password):
        return True
    return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes = 15)
    to_encode.update({'exp':expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt

def access_token(user: schemas.User):
    expire_token = timedelta(minutes=60)
    access_token = create_access_token(data = {'user_email': user.email}, expires_delta = expire_token)
    return access_token
