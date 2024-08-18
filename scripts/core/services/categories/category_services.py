import logging

from fastapi import Depends
from scripts.core.handler.categories_handler.category import CategoryHandler
from scripts.core.handler.sql_handler import get_db_session
from scripts.core.schemas.category import CategoryCreate
from scripts.core.services.categories import category_router
from scripts.utils.cookie_decorator import CookieDecorator, MetaInfoSchema
from sqlalchemy.orm import Session
from typing_extensions import Annotated

get_cookies = CookieDecorator()


@category_router.get("/categories")
def get_categories_list(
    db_session: Annotated[Session, Depends(get_db_session)],
    meta: MetaInfoSchema = Depends(get_cookies),
):
    try:
        return CategoryHandler(user_id=meta.user_id).get_category_list_for_user(
            db_session=db_session
        )
    except Exception as e:
        logging.exception(f"failed in getting categories for user as {e}")


@category_router.get("/categories/{id}")
def get_category_info_by_id(
    db_session: Annotated[Session, Depends(get_db_session)],
    meta: MetaInfoSchema = Depends(get_cookies),
    id: str = None,
):
    try:
        return CategoryHandler(user_id=meta.user_id).get_category_by_id(
            db_session=db_session, category_id=id
        )
    except Exception as e:
        logging.exception(f"failed in getting categories for user as {e}")


@category_router.post("/categories/create")
def create_category(
    create_category_payload: CategoryCreate,
    db_session: Annotated[Session, Depends(get_db_session)],
    meta: MetaInfoSchema = Depends(get_cookies),
):
    try:
        return CategoryHandler(user_id=meta.user_id).create_new_category(
            db_session=db_session, create_payload=create_category_payload
        )
    except Exception as e:
        logging.exception(f"failed in getting categories for user as {e}")


@category_router.put("/categories/update/{id}")
def update_category(
    update_category_payload: CategoryCreate,
    db_session: Annotated[Session, Depends(get_db_session)],
    meta: MetaInfoSchema = Depends(get_cookies),
    id: str = None,
):
    try:
        update_category_payload.category_id = id
        return CategoryHandler(user_id=meta.user_id).update_existing_category(
            db_session=db_session, update_payload=update_category_payload
        )
    except Exception as e:
        logging.exception(f"failed in getting categories for user as {e}")


@category_router.delete("/categories/delete/{id}")
def delete_category(
    db_session: Annotated[Session, Depends(get_db_session)],
    id: str = None,
    meta: MetaInfoSchema = Depends(get_cookies),
):
    try:
        return CategoryHandler(user_id=meta.user_id).delete_existing_category(
            db_session=db_session, category_id=id
        )
    except Exception as e:
        logging.exception(f"failed in getting categories for user as {e}")
