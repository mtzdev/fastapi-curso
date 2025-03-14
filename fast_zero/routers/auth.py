from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fast_zero.schemas import Token
from fast_zero.models import User
from fast_zero.security import create_access_token, verify_password
from fast_zero.database import get_session
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/token', response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail='Incorrect email or password')

    access_token = create_access_token({'sub': user.email})
    return {'access_token': access_token, 'token_type': 'Bearer'}