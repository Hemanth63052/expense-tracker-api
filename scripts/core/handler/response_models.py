from typing import Any, Optional

from pydantic import BaseModel


class DefaultResponse(BaseModel):
    status: str = "success"
    message: str = "success"
    data: Optional[Any] = []


class DefaultFailedResponse(BaseModel):
    status: str = "failed"
    message: Optional[str] = "failed"
    error: Optional[str] = "error"
