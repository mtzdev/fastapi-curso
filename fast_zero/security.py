from datetime import datetime, timedelta
from http import HTTPStatus
from fast_zero.models import User
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import encode, decode
from jwt.exceptions import PyJWTError
from pwdlib import PasswordHash
from zoneinfo import ZoneInfo

from fast_zero.database import get_session
from sqlalchemy import select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

pwd_context = PasswordHash.recommended()
SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_password_hash(plain_password: str):
    return pwd_context.hash(plain_password) # -> retorna a senha criptografada

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(payload: dict):
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({'exp': expire})

    return encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get('sub')
        if not email:
            raise credentials_exception

        user = session.scalar(select(User).where(User.email == email))
        if not user:
            raise credentials_exception

        return user
    except PyJWTError:
        raise credentials_exception