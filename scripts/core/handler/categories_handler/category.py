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
        """
        Retrieve the category list for a specific user.

        Args:
            db_session (Session): The database session.

        Returns:
            DefaultResponse: A response object containing the category list data and a success message.
        """
        sql_util = SQLUtil(session=db_session)
        data = sql_util.fetch_as_json(
            self.category_queries.get_category_query(user_id=self.user_id)
        )
        return DefaultResponse(data=data, message="success")

    def get_category_by_id(self, db_session: Session, category_id: str):
        """
        Retrieve the category list for a specific user by category id.

        Args:
            db_session (Session): The database session.
            category_id (str): The id of the category.

        Returns:
            DefaultResponse: A response object containing the category list data and a success message.
        """
        sql_util = SQLUtil(session=db_session)
        data = sql_util.fetch_as_json(
            self.category_queries.get_category_query(
                user_id=self.user_id, category_id=category_id
            )
        )
        return DefaultResponse(data=data, message="success")

    def create_new_category(self, db_session: Session, create_payload: CategoryCreate):
        """
        Create a new category for a specific user.
        Args:
            db_session (Session): The database session.
            create_payload (CategoryCreate): The payload for creating a new category.
        :returns
            DefaultResponse: A response object containing the created category data and a success message.
        """
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
        """
        Update an existing category for a specific user.
        Args:
            db_session (Session): The database session.
            update_payload (CategoryCreate): The payload for updating an existing category.
        :returns
            DefaultResponse: A response object containing the updated category data and a success message.
        """
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
        """
        Delete an existing category for a specific user.
        Args:
            db_session (Session): The database session.
            category_id (str): The id of the category to be deleted.
        :returns
            DefaultResponse: A response object containing a success message.
        """
        sql_util = SQLUtil(session=db_session)
        sql_util.delete_data(
            {"user_id": self.user_id, "category_id": category_id},
            table=CategoriesOrmSchema,
        )
        return DefaultResponse(message="Category deleted successfully")
