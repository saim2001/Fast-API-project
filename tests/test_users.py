import pytest
from app import schema
from jose import jwt
from app.config import settings
from .databse import client,session




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


@pytest.mark.parametrize('email, password, status_code',[
    ('wrongemail@gmail.com', 'password', 403),
    ('saim.rao62@yahoo.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password', 422),
    ('saim.rao62@gmailcom', None, 422)
])
def test_failed_login(client,email,password,status_code):
    res = client.post('/login',data={
        'username':email,
        'password':password
    })
    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid credentials'
