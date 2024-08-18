import logging

from fastapi import Depends
from scripts.core.handler.expense_handler.expenses import ExpenseHandler
from scripts.core.handler.response_models import DefaultFailedResponse
from scripts.core.handler.sql_handler import get_db_session
from scripts.core.schemas.expenses import CreateExpense
from scripts.core.services.expenses import expense_router
from scripts.utils.cookie_decorator import CookieDecorator, MetaInfoSchema
from sqlalchemy.orm import Session
from typing_extensions import Annotated

get_cookies = CookieDecorator()


@expense_router.get("/categories/{cid}/transactions/")
def get_categories_list(
    db_session: Annotated[Session, Depends(get_db_session)],
    meta: MetaInfoSchema = Depends(get_cookies),
    cid: str = None,
):
    try:
        return ExpenseHandler(user_id=meta.user_id).get_expenses_list_of_category(
            category_id=cid, db_session=db_session
        )
    except Exception as e:
        logging.exception(f"failed in getting expense for user as {e}")
        return DefaultFailedResponse(message="failed in getting expense for user")


@expense_router.get("/categories/{cid}/transactions/{tid}")
def get_category_info_by_id(
    db_session: Annotated[Session, Depends(get_db_session)],
    meta: MetaInfoSchema = Depends(get_cookies),
    cid: str = None,
    tid: str = None,
):
    try:
        return ExpenseHandler(meta.user_id).get_expense_by_category_and_expense_id(
            db_session=db_session, category_id=cid, expense_id=tid
        )
    except Exception as e:
        logging.exception(f"failed in getting expense for user as {e}")
        return DefaultFailedResponse(message="failed in getting expense for user")


@expense_router.post("/categories/create/transactions")
def create_category(
    create_category_payload: CreateExpense,
    db_session: Annotated[Session, Depends(get_db_session)],
    meta: MetaInfoSchema = Depends(get_cookies),
):
    try:
        return ExpenseHandler(meta.user_id).create_new_expense(
            db_session=db_session, create_payload=create_category_payload
        )
    except Exception as e:
        logging.exception(f"failed in creating expense for user as {e}")
        return DefaultFailedResponse(message="failed in creating expense for user")


@expense_router.put("/categories/{cid}/transactions/{tid}")
def update_category(
    update_expense_payload: CreateExpense,
    db_session: Annotated[Session, Depends(get_db_session)],
    meta: MetaInfoSchema = Depends(get_cookies),
    cid: str = None,
    tid: str = None,
):
    try:
        update_expense_payload.category_id = cid
        update_expense_payload.expense_id = tid
        return ExpenseHandler(meta.user_id).update_existing_expense(
            db_session=db_session, update_payload=update_expense_payload
        )
    except Exception as e:
        logging.exception(f"failed in updating expense for user as {e}")
        return DefaultFailedResponse(message="failed in updating expense for user")


@expense_router.delete("/categories/{cid}/transactions/{tid}")
def delete_category(
    db_session: Annotated[Session, Depends(get_db_session)],
    cid: str = None,
    meta: MetaInfoSchema = Depends(get_cookies),
    tid: str = None,
):
    try:
        return ExpenseHandler(meta.user_id).delete_existing_expense(
            db_session=db_session, expense_id=tid, category_id=cid
        )
    except Exception as e:
        logging.exception(f"failed in deleting expense for user as {e}")
        return DefaultFailedResponse(message="failed in deleting expense for user")
