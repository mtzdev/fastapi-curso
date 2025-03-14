from http import HTTPStatus
from fast_zero.security import create_access_token, SECRET_KEY, ALGORITHM
from jwt import decode

def test_jwt():
    payload = {'sub': 'test'}
    result = create_access_token(payload)
    decoded = decode(result, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded['sub'] == payload['sub']
    assert decoded['exp']

def test_jwt_invalid_token(client):
    response = client.delete('/users/1', headers={'Authorization': 'Bearer invalid-token'})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}

def test_get_current_user_not_found(client):
    token = create_access_token({'a': 'b'})
    response = client.delete('/users/1', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}

def test_get_current_user_does_not_exist(client):
    token = create_access_token({'sub': 'test@test.com'})
    response = client.delete('/users/1', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}