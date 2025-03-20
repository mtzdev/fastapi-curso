from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import encode, decode
from jwt.exceptions import PyJWTError
from pwdlib import PasswordHash
from sqlalchemy import select
from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.settings import Settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')
settings = Settings()
pwd_context = PasswordHash.recommended()

def get_password_hash(plain_password: str):
    return pwd_context.hash(plain_password) # -> retorna a senha criptografada

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(payload: dict):
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({'exp': expire})

    return encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def get_current_user(session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get('sub')
        if not email:
            raise credentials_exception

        user = session.scalar(select(User).where(User.email == email))
        if not user:
            raise credentials_exception

        return user
    except PyJWTError:
        raise credentials_exception