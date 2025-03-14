from fast_zero.security import get_password_hash, get_current_user
from fastapi import APIRouter, Depends, HTTPException
from fast_zero.schemas import Message, UserPublic, UserSchema, UserList
from fast_zero.models import User
from fast_zero.database import get_session
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter(prefix='/users', tags=['users'])

@router.get('/', response_model=UserList)
def read_users(skip_to: int = 0, limit: int = 6, session = Depends(get_session)):
    user = session.scalars(select(User).offset(skip_to).limit(limit))
    return {'users': user}

@router.get('/{user_id}', response_model=UserPublic)
def get_user(user_id: int, session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user

@router.post('/', status_code=201, response_model=UserPublic)
def create_user(user: UserSchema, session = Depends(get_session)):
    db_user = session.scalar(select(User).where((User.username == user.username) | (User.email == user.email)))

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(status_code=400, detail='Username already exists')
        elif db_user.email == user.email:
            raise HTTPException(status_code=400, detail='Email already exists')

    db_user = User(username=user.username, email=user.email, password=get_password_hash(user.password))
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.put('/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session = Depends(get_session), current_user = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='Not enough permission!')

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)
    session.commit()
    session.refresh(current_user)

    return current_user

@router.delete('/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session), current_user = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='Not enough permission!')

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}