from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app import auth, db
from app.models import TokenResponse

router = APIRouter(prefix="/api", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest) -> TokenResponse:
    user = db.get_user_by_email(request.email)
    if user is None or user["password"] != request.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return TokenResponse(access_token=auth.create_access_token(user["id"]))
