import pytest
from app import models
from fastapi.testclient import TestClient
from app.main import app
from app import schema
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.database import get_db



SQLALCHEMY_DATABASE_URL = 'cockroachdb://saim:Qv9Nkm3AJTQoq4MfnMjHfw@redear-giraffe-8487.8nk.gcp-asia-southeast1.cockroachlabs.cloud:26257/fast_api_test_db?sslmode=verify-full'


engine = create_engine(SQLALCHEMY_DATABASE_URL)
testingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)




# Dependency

@pytest.fixture()
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = testingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):

    
    def override_get_db():
        
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

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
