"""
Security regression tests for the demo-login flow: verifies the
privilege-escalation fix (self-declared "admin" role must be rejected) and
basic input validation stay in place.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from starlette.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_demo_login_rejects_admin_role_self_assignment():
    r = client.post("/api/auth/demo-login", json={"email": "attacker@example.com", "role": "admin"})
    assert r.status_code == 422


def test_demo_login_rejects_arbitrary_role_strings():
    r = client.post("/api/auth/demo-login", json={"email": "attacker@example.com", "role": "super-admin"})
    assert r.status_code == 422


def test_demo_login_accepts_member_role():
    r = client.post("/api/auth/demo-login", json={"email": "carl@example.com", "role": "member"})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_demo_login_rejects_invalid_email():
    r = client.post("/api/auth/demo-login", json={"email": "not-an-email", "role": "member"})
    assert r.status_code == 422


def test_issued_token_cannot_self_grant_admin_via_require_role():
    """
    End-to-end check: a token minted through the public demo-login flow
    should never carry admin/elevated privileges, regardless of role
    checks performed downstream.
    """
    r = client.post("/api/auth/demo-login", json={"email": "carl@example.com", "role": "member"})
    token = r.json()["access_token"]

    from app.core.security import decode_token
    payload = decode_token(token)
    assert payload["role"] != "admin"
