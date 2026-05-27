from tests.conftest import auth_headers


def test_register_success(client):
    res = client.post("/api/v1/auth/register", json={
        "email": "user@test.com",
        "full_name": "Test User",
        "password": "password123",
        "role": "employee"
    })
    assert res.status_code == 201
    data = res.json()
    assert data["email"] == "user@test.com"
    assert data["role"] == "employee"
    assert "hashed_password" not in data


def test_register_duplicate_email(client):
    payload = {
        "email": "user@test.com",
        "full_name": "Test User",
        "password": "password123",
        "role": "employee"
    }
    client.post("/api/v1/auth/register", json=payload)
    res = client.post("/api/v1/auth/register", json=payload)
    assert res.status_code == 400
    assert "already registered" in res.json()["detail"]


def test_login_success(client):
    client.post("/api/v1/auth/register", json={
        "email": "user@test.com",
        "full_name": "Test User",
        "password": "password123",
        "role": "employee"
    })
    res = client.post("/api/v1/auth/login", json={
        "email": "user@test.com",
        "password": "password123"
    })
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_login_wrong_password(client):
    client.post("/api/v1/auth/register", json={
        "email": "user@test.com",
        "full_name": "Test User",
        "password": "password123",
        "role": "employee"
    })
    res = client.post("/api/v1/auth/login", json={
        "email": "user@test.com",
        "password": "wrongpassword"
    })
    assert res.status_code == 401


def test_login_nonexistent_user(client):
    res = client.post("/api/v1/auth/login", json={
        "email": "ghost@test.com",
        "password": "password123"
    })
    assert res.status_code == 401


def test_get_me(client, registered_employee):
    res = client.get(
        "/api/v1/users/me",
        headers=auth_headers(registered_employee)
    )
    assert res.status_code == 200
    assert res.json()["email"] == "employee@test.com"


def test_get_me_unauthenticated(client):
    res = client.get("/api/v1/users/me")
    assert res.status_code == 401