from http import HTTPStatus
from fast_zero.schemas import UserPublic

def test_read_root_http_status_ok(client):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK

def test_read_root_response(client):
    response = client.get("/")
    assert response.json() == {"message": "Nothing available here"}
