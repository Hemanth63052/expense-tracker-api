import logging

from fastapi import Depends, Request, Response
from scripts.core.handler.response_models import DefaultFailedResponse
from scripts.core.handler.sql_handler import get_db_session
from scripts.core.handler.user_handler import AuthenticationHandler
from scripts.core.schemas.user_auth_schemas import LoginSchema, SignUpSchema
from scripts.core.services.user_auth import user_router
from sqlalchemy.orm import Session


@user_router.post("/signup")
def signup(
    sign_up_payload: SignUpSchema, db_session: Session = Depends(get_db_session)
):
    try:
        return AuthenticationHandler().signup(
            request_payload=sign_up_payload, db_session=db_session
        )
    except Exception as e:
        logging.info(f"Failed in sign up as {e}")
        return DefaultFailedResponse(message=f"{e}")


@user_router.post("/login")
def login(
    login_payload: LoginSchema,
    request: Request,
    response: Response,
    db_session: Session = Depends(get_db_session),
):
    try:
        return AuthenticationHandler().login(
            login_payload=login_payload,
            request=request,
            response=response,
            db_session=db_session,
        )

    except Exception as e:
        logging.info("Failed in Login")
        return DefaultFailedResponse(message=f"{e}")
