import base64
import logging
import uuid
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, Request, Response, status
from scripts.core.handler.response_models import DefaultResponse
from scripts.core.schemas.user_auth_schemas import LoginSchema, SignUpSchema
from scripts.core.sql_queries import SQLQueries
from scripts.db.sql_table_orm_schemas import UserDetailsOrmSchema
from scripts.utils.enc_dec_util import EncrDecUtil
from scripts.utils.sql_util import SQLUtil
from sqlalchemy.orm import Session


class AuthenticationHandler:
    def __init__(self):
        self.encry_decry_util = EncrDecUtil()

    def signup(self, request_payload: SignUpSchema, db_session: Session):
        """
        Create a new user account.
        Args:
            db_session (Session): The database session.
            request_payload (SignUpSchema): The payload for creating a new user account.
        :returns
            DefaultResponse: A response object containing the created user data and a success message.
        """
        try:
            sql_util = SQLUtil(session=db_session)
            if sql_util.fetch_as_json(
                SQLQueries.get_user_details_by_email(request_payload.email)
            ):
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail="Email Already exists",
                )
            request_payload.password = self.encry_decry_util.encrypt_password(
                request_payload.password
            ).decode("utf-8")
            sql_util.insert_into_postgres_using_session(
                request_payload.model_dump(), pg_table=UserDetailsOrmSchema
            )
            return DefaultResponse(
                **{"message": "Sign Up successful. Please Login", "data": []}
            )
        except Exception as e:
            logging.exception(f"Error in sign up as {e}")
            raise HTTPException(
                status_code=status.HTTP_417_EXPECTATION_FAILED,
                detail="Oops ! Failed in sign up. Please contact " "Support Team",
            )

    def login(
        self,
        login_payload: LoginSchema,
        request: Request,
        response: Response,
        db_session,
    ):
        """
        Log in to an existing user account.
        Args:
            login_payload (LoginSchema): The payload for logging in to an existing user account.
            request (Request): The request object.
            response (Response): The response object.
            db_session (Session): The database session.
        :returns
            DefaultResponse: A response object containing the logged in user data and a success message.
        """
        try:
            sql_util = SQLUtil(session=db_session)
            data = sql_util.fetch_as_json(
                SQLQueries.get_user_details_by_email(login_payload.email)
            )
            if not data:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="User Not found"
                )
            password = base64.b64decode(login_payload.password[3:]).decode("utf-8")
            if (
                self.encry_decry_util.decrypt_password(data[0]["password"]) != password
                or data[0]["email"] != login_payload.email
            ):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Please enter valid password",
                )
            self.create_token(
                response=response,
                user_id=data[0]["user_id"],
                ip=request.client.host,
                password=password,
            )
            response.set_cookie("user_id", data[0]["user_id"])
            return DefaultResponse(**{"message": "Log in successful.", "data": []})
        except Exception as e:
            logging.exception(f"Oops! Failed to login as {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorised"
            )

    @staticmethod
    def create_token(
        response: Response,
        user_id: str,
        ip: str,
        password: str,
        age=30,
        login_token: str = None,
        token="8674cd1d-2578-4a62-8ab7-d3ee5f9a",
    ):
        """
        Create a token for the user.
        Args:
            response (Response): The response object.
            user_id (str): The id of the user.
            ip (str): The ip address of the user.
            password (str): The password of the user.
            age (int, optional): The age of the token. Defaults to 30.
            login_token (str, optional): The login token. Defaults to None.
            token (str, optional): The token. Defaults to "8674cd1d-2578-4a62-8ab7-d3ee5f9a".
        """
        uid = login_token
        if not uid:
            uid = str(uuid.uuid4()).replace("-", "")
        payload = {
            "ip": ip,
            "user_id": user_id,
            "token": token,
            "uid": uid,
            "age": age,
            "password": password,
        }
        exp = datetime.now(timezone.utc) + timedelta(minutes=age)
        _extras = {"iss": "hemanth", "exp": exp}
        _payload = payload | _extras
        encoded_payload = jwt.encode(
            _payload, key="Allgoodnamesaregone", algorithm="HS256"
        )
        response.set_cookie(
            "login-token",
            encoded_payload,
            samesite="strict",
            httponly=True,
            max_age=30 * 60,
            secure=True,
        )
        response.headers["login-token"] = encoded_payload
        return response
