from fastapi.testclient import TestClient
from fast_zero.app import app
from fast_zero.models import User, table_registry
from pytest import fixture
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

@fixture()
def client():
    return TestClient(app)

@fixture()
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


def test_create_user(session):
    user = User(
        username='testusername',
        email='test@email.com',
        password='password'
    )

    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == 'test@email.com')
    )
    assert result.username == 'testusername'