from fastapi import APIRouter, Depends
from fast_zero.database import get_session
from fast_zero.security import get_current_user
from fast_zero.schemas import TodoSchema, TodoPublic, TodoList
from fast_zero.models import User, Todo, TodoState
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter(prefix='/todos', tags=['todos'])

@router.post('/', status_code=200, response_model=TodoPublic)
def create_todo(todo: TodoSchema, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    db_todo = Todo(todo.title, todo.description, todo.state, user_id=user.id)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

@router.get('/', response_model=TodoList)
def list_todos(
        session: Session = Depends(get_session), user: User = Depends(get_current_user),
        title: str | None = None, description: str | None = None, state: TodoState | None = None,
        offset: int = 0, limit: int = 10):

    query = select(Todo).where(Todo.user_id == user.id)
    if title:
        query = query.filter(Todo.title.contains(title))
    if description:
        query = query.filter(Todo.description.contains(description))
    if state:
        query = query.filter(Todo.state == state)

    todos = session.scalars(query.offset(offset).limit(limit))
    return {'todos': todos}
