from typing import Annotated

import requests
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, HttpUrl

from app.auth import get_current_user
from app.models import User

router = APIRouter(prefix="/api", tags=["webhooks"])


class PreviewRequest(BaseModel):
    callback_url: HttpUrl


@router.post("/webhooks/vendor-preview")
def preview_vendor_webhook(
    request: PreviewRequest,
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.role != "staff":
        raise HTTPException(status_code=403, detail="Staff only")

    response = requests.get(str(request.callback_url), timeout=2)
    return {
        "status_code": response.status_code,
        "content_type": response.headers.get("content-type"),
        "preview": response.text[:200],
    }
