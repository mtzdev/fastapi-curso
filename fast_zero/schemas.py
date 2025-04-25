from pydantic import BaseModel, EmailStr, ConfigDict
from fast_zero.models import TodoState

class Message(BaseModel):
    message: str

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)

class UserList(BaseModel):
    users: list[UserPublic]

class Token(BaseModel):
    access_token: str  # token jwt
    token_type: str  # modelo de autorização

class TodoSchema(BaseModel):
    title: str
    description: str | None = None
    state: TodoState

class TodoPublic(TodoSchema):
    id: int

class TodoList(BaseModel):
    todos: list[TodoPublic]

class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None