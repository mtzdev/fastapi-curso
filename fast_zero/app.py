from fastapi import FastAPI, HTTPException
from fast_zero.schemas import Message, UserPublic, UserSchema, UserDb, UserList

app = FastAPI()

db = []

@app.get("/", status_code=200, response_model=Message)
def root():
    return {'message': 'Nothing available here'}

@app.get('/users', response_model=UserList)
def read_users():
    return {'users': db}

@app.post('/users', status_code=201, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDb(**user.model_dump(), id=len(db) + 1)
    db.append(user_with_id)
    return user_with_id

@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(db) or user_id < 1:
        raise HTTPException(status_code=404, detail='User not found')

    user_with_id = UserDb(**user.model_dump(), id=user_id)
    db[user_id - 1] = user_with_id
    return user_with_id

@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(db) or user_id < 1:
        raise HTTPException(status_code=404, detail='User not found')

    db.pop(user_id - 1)
    return {'message': 'User deleted'}