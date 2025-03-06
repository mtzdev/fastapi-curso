from http import HTTPStatus
from fast_zero.schemas import UserPublic

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
    assert response.json() == {"users": []}

def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get("/users")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}

def test_update_user(client, user):
    response = client.put("/users/1", json={
        "username": "newusername2",
        "email": "new@email.com",
        "password": "password",
        "id": 1
    })

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "newusername2",
        "email": "new@email.com",
        "id": 1
    }

def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}

def test_create_user_error_username_duplicated(client, user):
    response = client.post("/users", json={
        "username": "testusername",
        "password": "test2password",
        "email": "test2@gmail.com"
    })
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Username already exists"}

def test_create_user_error_email_duplicated(client, user):
    response = client.post("/users", json={
        "username": "test2username",
        "password": "test2password",
        "email": "test@gmail.com"
    })
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Email already exists"}

def test_delete_user_error_not_found(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}

def test_update_user_error_not_found(client):
    response = client.put("/users/1", json={
        "username": "test",
        "email": "test@gmail.com",
        "password": "test"
    })

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}

def test_get_user(client, user):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": "testusername",
        "email": "test@gmail.com"
    }

def test_get_user_error_not_found(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}