from typing import Annotated

from fastapi import APIRouter, Depends

from app import db
from app.auth import get_current_user
from app.models import User

router = APIRouter(prefix="/api", tags=["search"])


@router.get("/search")
def search_records(
    q: str,
    current_user: Annotated[User, Depends(get_current_user)],
):
    return {"results": db.search_records(q)}
