from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security import APIKeyCookie
from fastapi.security.api_key import APIKeyBase
from fastapi import Response, Request, HTTPException, status
import logging as logger
import jwt
from scripts.core.handler.sql_handler import get_db_session

from scripts.core.sql_queries import SQLQueries
from scripts.utils.enc_dec_util import EncrDecUtil
from scripts.utils.sql_util import SQLUtil


class CookieAuthentication(APIKeyBase):
    """
    Authentication backend using a cookie.
    Internally, uses a JWT token to store the data.
    """

    scheme: APIKeyCookie
    cookie_name: str
    cookie_secure: bool

    def __init__(
            self,
            cookie_name: str = "login-token",
    ):
        super().__init__()
        self.model: APIKey = APIKey(**{"in": APIKeyIn.cookie}, name=cookie_name)
        self.scheme_name = self.__class__.__name__
        self.cookie_name = cookie_name
        self.scheme = APIKeyCookie(name=self.cookie_name, auto_error=False)
        self.encry_decry_util = EncrDecUtil()

    def __call__(self, request: Request, response: Response) -> str:
        cookies = request.cookies
        login_token = cookies.get("login-token")
        if not login_token:
            login_token = request.headers.get("login-token")
        if not login_token:
            logger.info("CASE-0")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        login_token = jwt.decode(login_token,  key="Allgoodnamesaregone", algorithms="HS256")
        sql_util = SQLUtil(session=get_db_session())
        data=sql_util.fetch_as_json(SQLQueries.get_details_by_user_id(login_token.get("user_id")))
        if not data:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User Not found")
        if self.encry_decry_util.decrypt_password(data[0]['password']) != login_token.get('password'):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Please enter valid password")
        response.set_cookie(
            "login-token",
            cookies.get("login-token"),
            samesite="strict",
            httponly=True,
            secure=True,
            max_age=30* 60,
        )
        return login_token.get("user_id")


