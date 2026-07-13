from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, field_validator

from app.core.security import create_access_token
from app.core.config import settings

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Demo login can only mint low-privilege roles. "admin" (and any other role)
# must come from a real identity provider (Slack OAuth), never from a
# self-declared value in a request body - otherwise any caller could mint
# an admin JWT for themselves.
SELF_ASSIGNABLE_ROLES = {"viewer", "member"}


class DemoLoginRequest(BaseModel):
    email: EmailStr
    role: str = "member"

    @field_validator("role")
    @classmethod
    def role_must_be_self_assignable(cls, value: str) -> str:
        if value not in SELF_ASSIGNABLE_ROLES:
            raise ValueError(
                f"role must be one of {sorted(SELF_ASSIGNABLE_ROLES)}; "
                "elevated roles can only be granted via Slack OAuth"
            )
        return value


@router.post("/demo-login")
def demo_login(request: DemoLoginRequest):
    """
    Demo-mode login that issues a JWT without a real identity provider.
    Restricted to non-privileged roles - see SELF_ASSIGNABLE_ROLES above.
    Production auth uses Slack OAuth (see /api/auth/slack/callback) and
    exchanges the Slack identity for the same JWT shape.
    """
    token = create_access_token(subject=request.email, role=request.role)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/slack/callback")
def slack_oauth_callback(code: str = ""):
    """
    Slack OAuth callback stub. In production this exchanges `code` for an
    access token via https://slack.com/api/oauth.v2.access using
    SLACK_CLIENT_ID / SLACK_CLIENT_SECRET, resolves the Slack user identity,
    and issues a JWT scoped to that user's workspace role.
    """
    if not settings.SLACK_CLIENT_ID:
        raise HTTPException(status_code=501, detail="Slack OAuth not configured. Set SLACK_CLIENT_ID/SECRET.")
    token = create_access_token(subject="slack-user", role="member")
    return {"access_token": token, "token_type": "bearer"}
