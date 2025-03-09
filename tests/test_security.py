from fast_zero.security import create_access_token, SECRET_KEY, ALGORITHM
from jwt import decode

def test_jwt():
    payload = {'sub': 'test'}
    result = create_access_token(payload)
    decoded = decode(result, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded['sub'] == payload['sub']
    assert decoded['exp']