from fastapi import FastAPI
from fast_zero.schemas import Message
from fast_zero.routers import users, auth, todo

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todo.router)

@app.get("/", status_code=200, response_model=Message)
def root():
    return {'message': 'Nothing available here'}
