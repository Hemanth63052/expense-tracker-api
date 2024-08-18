from fastapi import HTTPException, status
from scripts.core.handler.categories_handler.category_queries import \
    CategoryQueries
from scripts.core.handler.response_models import DefaultResponse
from scripts.core.schemas.category import CategoryCreate
from scripts.db.sql_table_orm_schemas import CategoriesOrmSchema
from scripts.utils.sql_util import SQLUtil
from sqlalchemy.orm import Session


class CategoryHandler:

    def __init__(self, user_id):
        self.user_id = user_id
        self.category_queries = CategoryQueries()

    def get_category_list_for_user(self, db_session: Session):
        sql_util = SQLUtil(session=db_session)
        data = sql_util.fetch_as_json(
            self.category_queries.get_category_query(user_id=self.user_id)
        )
        return DefaultResponse(data=data, message="success")

    def get_category_by_id(self, db_session: Session, category_id: str):
        sql_util = SQLUtil(session=db_session)
        data = sql_util.fetch_as_json(
            self.category_queries.get_category_query(
                user_id=self.user_id, category_id=category_id
            )
        )
        return DefaultResponse(data=data, message="success")

    def create_new_category(self, db_session: Session, create_payload: CategoryCreate):
        create_payload.user_id = self.user_id
        sql_util = SQLUtil(session=db_session)
        data = sql_util.fetch_as_json(
            self.category_queries.get_category_query(
                user_id=self.user_id, title=create_payload.title
            )
        )
        if data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category is already exists",
            )
        sql_util.insert_into_postgres_using_session(
            create_payload.model_dump(), CategoriesOrmSchema
        )
        return DefaultResponse(message="Category creation success")

    def update_existing_category(
        self, db_session: Session, update_payload: CategoryCreate
    ):
        update_payload.user_id = self.user_id
        sql_util = SQLUtil(session=db_session)
        data = sql_util.fetch_as_json(
            self.category_queries.get_category_query(
                user_id=self.user_id, category_id=update_payload.category_id
            )
        )
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Category Id not found"
            )
        query_dict = {
            "user_id": self.user_id,
            "category_id": update_payload.category_id,
        }
        sql_util.update_postgres_columns(
            filter_dict=query_dict,
            update_dict=update_payload.model_dump(),
            table=CategoriesOrmSchema,
        )
        return DefaultResponse(message="Category Updated Successfully")

    def delete_existing_category(self, db_session: Session, category_id: str):
        sql_util = SQLUtil(session=db_session)
        sql_util.delete_data(
            {"user_id": self.user_id, "category_id": category_id},
            table=CategoriesOrmSchema,
        )
        return DefaultResponse(message="Category deleted successfully")
