from pydantic import BaseModel


class User(BaseModel):
    id: str
    email: str
    role: str = "member"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
