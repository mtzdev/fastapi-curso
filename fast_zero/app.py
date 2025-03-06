from fast_zero.database import get_session
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException
from fast_zero.schemas import Message, UserPublic, UserSchema, UserList
from fast_zero.models import User

app = FastAPI()

@app.get("/", status_code=200, response_model=Message)
def root():
    return {'message': 'Nothing available here'}

@app.get('/users/{user_id}', response_model=UserPublic)
def get_user(user_id: int, session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user

@app.get('/users', response_model=UserList)
def read_users(skip_to: int = 0, limit: int = 6, session = Depends(get_session)):
    user = session.scalars(select(User).offset(skip_to).limit(limit))
    return {'users': user}

@app.post('/users', status_code=201, response_model=UserPublic)
def create_user(user: UserSchema, session = Depends(get_session)):
    db_user = session.scalar(select(User).where((User.username == user.username) | (User.email == user.email)))

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(status_code=400, detail='Username already exists')
        elif db_user.email == user.email:
            raise HTTPException(status_code=400, detail='Email already exists')

    db_user = User(username=user.username, email=user.email, password=user.password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session = Depends(get_session)):
    db_user: UserSchema = session.scalar(select(User).where(User.id == user_id))   # ou: session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password
    session.commit()
    session.refresh(db_user)
    return db_user

@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')

    session.delete(db_user)
    session.commit()

    return {'message': 'User deleted'}
