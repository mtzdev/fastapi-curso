from http import HTTPStatus
from fastapi.testclient import TestClient
from fast_zero.app import app
from pytest import fixture

@fixture()
def client():
    return TestClient(app)

def test_read_root_http_status_ok(client):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK

def test_read_root_response(client):
    response = client.get("/")
    assert response.json() == {"message": "Nothing available here"}

def test_create_user(client):
    response = client.post("/users", json={
        "username": "testusername",
        "password": "password",
        "email": "email@test.com"
    })
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "testusername",
        "email": "email@test.com",
        "id": 1
    }

def test_read_users(client):
    response = client.get("/users")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [
        {
            "username": "testusername",
            "email": "email@test.com",
            "id": 1
        }
    ]}

def test_update_user(client):
    response = client.put("/users/1", json={
        "username": "newusername",
        "email": "new@email.com",
        "password": "password",
        "id": 1
    })

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "newusername",
        "email": "new@email.com",
        "id": 1
    }


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}