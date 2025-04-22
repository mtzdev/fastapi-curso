from http import HTTPStatus

from freezegun import freeze_time

def test_get_token(client, user):
    response = client.post('/auth/token', data={'username': user.email, 'password': user.clean_password})
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token

def test_token_expired_after_time(client, user):
    with freeze_time('2023-01-01 12:00:00'):
        response = client.post('/auth/token', data={'username': user.email, 'password': user.clean_password})

        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-01-01 12:31:00'):
        response = client.put('/users/1', headers={'Authorization': f'Bearer {token}'}, json={
            'username': 'newusername',
            'email': 'new@email.com',
            'password': 'newpassword'
        })

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}

def test_token_wrong_password(client, user):
    response = client.post('/auth/token', data={'username': user.email, 'password': 'wrong_password'})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}

def test_token_wrong_email(client, user):
    response = client.post('/auth/token', data={'username': 'email@wrong.com', 'password': user.clean_password})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_refresh_token(client, user, token):
    response = client.post('/auth/refresh-token', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json()['token_type'] == 'Bearer'
    assert 'access_token' in response.json()

def test_refresh_token_expired(client, user):
    with freeze_time('2023-01-01 12:00:00'):
        response = client.post('/auth/token', data={'username': user.email, 'password': user.clean_password})

        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-01-01 12:31:00'):
        response = client.post('/auth/refresh-token', headers={'Authorization': f'Bearer {token}'})

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}

