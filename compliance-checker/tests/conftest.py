import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import Base, get_db

# Use a separate SQLite database for tests — no Docker needed
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def registered_admin(client):
    client.post("/api/v1/auth/register", json={
        "email": "admin@test.com",
        "full_name": "Test Admin",
        "password": "password123",
        "role": "admin"
    })
    res = client.post("/api/v1/auth/login", json={
        "email": "admin@test.com",
        "password": "password123"
    })
    return res.json()


@pytest.fixture()
def registered_employee(client):
    client.post("/api/v1/auth/register", json={
        "email": "employee@test.com",
        "full_name": "Test Employee",
        "password": "password123",
        "role": "employee"
    })
    res = client.post("/api/v1/auth/login", json={
        "email": "employee@test.com",
        "password": "password123"
    })
    return res.json()


def auth_headers(token_data):
    return {"Authorization": f"Bearer {token_data['access_token']}"}