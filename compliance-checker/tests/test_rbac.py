from tests.conftest import auth_headers


def test_admin_can_list_users(client, registered_admin):
    res = client.get(
        "/api/v1/users/",
        headers=auth_headers(registered_admin)
    )
    assert res.status_code == 200


def test_employee_cannot_list_users(client, registered_employee):
    res = client.get(
        "/api/v1/users/",
        headers=auth_headers(registered_employee)
    )
    assert res.status_code == 403


def test_admin_can_update_role(client, registered_admin, registered_employee):
    employee_id = registered_employee["user"]["id"]
    res = client.patch(
        f"/api/v1/users/{employee_id}/role",
        json={"role": "compliance_officer"},
        headers=auth_headers(registered_admin)
    )
    assert res.status_code == 200
    assert res.json()["role"] == "compliance_officer"


def test_employee_cannot_update_role(client, registered_admin, registered_employee):
    admin_id = registered_admin["user"]["id"]
    res = client.patch(
        f"/api/v1/users/{admin_id}/role",
        json={"role": "employee"},
        headers=auth_headers(registered_employee)
    )
    assert res.status_code == 403


def test_unauthenticated_cannot_access_protected_routes(client):
    res = client.get("/api/v1/users/")
    assert res.status_code == 401


def test_employee_cannot_access_audit_logs(client, registered_employee):
    res = client.get(
        "/api/v1/audit-logs/",
        headers=auth_headers(registered_employee)
    )
    assert res.status_code == 403


def test_employee_can_access_own_audit_logs(client, registered_employee):
    res = client.get(
        "/api/v1/audit-logs/me",
        headers=auth_headers(registered_employee)
    )
    assert res.status_code == 200