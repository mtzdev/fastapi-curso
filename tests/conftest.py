from contextlib import contextmanager
from datetime import datetime
import factory
import factory.fuzzy
from fast_zero.security import get_password_hash
from fastapi.testclient import TestClient
from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import TodoState, table_registry, User, Todo
from pytest import fixture
from sqlalchemy import StaticPool, create_engine, event
from sqlalchemy.orm import Session

class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'testuser{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}:password-test  ')

class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker('text')
    description = factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1

@fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()

@fixture()
def session():
    engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)

@fixture()
def user(session: Session):
    user = UserFactory(password=get_password_hash('testpassword'))
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'testpassword'
    return user

@fixture()
def other_user(session: Session):
    user = UserFactory()
    session.add(user)
    session.commit()
    session.refresh(user)

    return user

@fixture()
def token(client, user):
    response = client.post('/auth/token', data={'username': user.email, 'password': user.clean_password})
    return response.json()['access_token']

@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    def fake_time_handler(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_handler)
    yield time
    event.remove(model, 'before_insert', fake_time_handler)


@fixture
def mock_db_time():
    return _mock_db_time