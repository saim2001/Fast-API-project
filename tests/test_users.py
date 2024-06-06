import pytest
from app import schema
from jose import jwt
from app.config import settings
from .databse import client,session

@pytest.fixture
def test_user(client):
    user_data = {
        'username':'saim89',
        'email':'saim.rao62@yahoo.com',
        'password':'psw11122'
    }
    res = client.post('/users/',json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user



def test_create_user(client):
    res = client.post('/users/',json={
        'username':'saim89',
        'email':'saim.rao62@yahoo.com',
        'password':'psw11122'
    })
    print(res.json())
    new_user = schema.UserResp(**res.json())
    assert new_user.email == 'saim.rao62@yahoo.com'
    assert res.status_code == 201

def test_login(client,test_user):
    res = client.post('/login',data={
        'username':test_user['email'],
        'password':test_user['password']
    })
    login_res = schema.Token(**res.json())
    payload = jwt.decode(login_res.access_token,settings.secret_key,algorithms=[settings.algorithm])
    id: str = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200
