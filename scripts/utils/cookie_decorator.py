from fastapi import Response, Request
from pydantic import BaseModel
class MetaInfoSchema(BaseModel):
    user_id: str

class CookieDecorator:

    async def __call__(self, request: Request, response: Response):
        cookies = request.cookies
        cookie_json = {
            "user_id": cookies.get("user_id", request.headers.get("user_id")),
        }
        return MetaInfoSchema(**cookie_json)
