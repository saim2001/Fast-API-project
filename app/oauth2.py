from jose import jwt,JWTError
# from dotenv import dotenv_values
from datetime import datetime,timedelta
from fastapi import status,HTTPException,Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from .config import settings

from . import schema

# config = dotenv_values()

oAuth2 = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    
    to_encode = data.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_time)
    to_encode["exp"] = expire_time
    encoded_jwt = jwt.encode(to_encode,settings.secret_key,algorithm=settings.algorithm)

    return encoded_jwt

def verify_access_token(token:str, credential_exception):

    try:
        payload = jwt.decode(token,settings.secret_key,algorithms=[settings.algorithm])
        id: str = payload.get("user_id")
        # print(type(id))
        if id is None:
            raise credential_exception
        token_data = schema.TokenData(id=id)
    except JWTError:
        raise credential_exception
    return token_data

def get_current_user(token:str = Depends(oAuth2)):

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate':'Bearer'}
    )

    return verify_access_token(token,credential_exception)


