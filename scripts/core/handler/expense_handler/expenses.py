from fastapi import HTTPException, status
from scripts.core.handler.expense_handler.expense_queries import ExpenseQueries
from sqlalchemy.orm import Session

from scripts.core.handler.response_models import DefaultResponse
from scripts.core.schemas.expenses import CreateExpense
from scripts.db.sql_table_orm_schemas import TransactionOrmSchema
from scripts.utils.sql_util import SQLUtil


class ExpenseHandler:

    def __init__(self, user_id):
        self.user_id = user_id
        self.expense_queries = ExpenseQueries()

    def get_expense_list_for_user(self, db_session: Session):
        sql_util = SQLUtil(session=db_session)
        data = sql_util.fetch_as_json(self.expense_queries.get_expense_query(user_id=self.user_id))
        return DefaultResponse(data=data, message="success")

    def get_expense_by_category_and_expense_id(self, db_session: Session,
                                               category_id: str,
                                               expense_id: str):
        sql_util = SQLUtil(session=db_session)
        data = sql_util.fetch_as_json(
            self.expense_queries.get_expense_query(user_id=self.user_id,
                                                   category_id=category_id,
                                                   expense_id=expense_id))
        return DefaultResponse(data=data, message="success")

    def get_expenses_list_of_category(self, db_session: Session, category_id: str):
        sql_util = SQLUtil(session=db_session)
        data = sql_util.fetch_as_json(
            self.expense_queries.get_expense_query(user_id=self.user_id, category_id=category_id))
        return DefaultResponse(data=data, message="success")

    def get_expense_by_id(self, db_session: Session, expense_id: str):
        sql_util = SQLUtil(session=db_session)
        data = sql_util.fetch_as_json(self.expense_queries.get_expense_query(user_id=self.user_id, expense_id=expense_id))
        return DefaultResponse(data=data, message="success")

    def create_new_expense(self, db_session: Session, create_payload: CreateExpense):
        create_payload.user_id = self.user_id
        sql_util = SQLUtil(session=db_session)
        data = sql_util.fetch_as_json(
            self.expense_queries.get_expense_query(user_id=self.user_id,
                                                   expense_name=create_payload.expense_name))
        if data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Expense Already exists")
        sql_util.insert_into_postgres_using_session(create_payload.model_dump(),
                                                    TransactionOrmSchema)
        return DefaultResponse(message="Category creation success")

    def update_existing_expense(self, db_session: Session, update_payload:CreateExpense):
        update_payload.user_id=self.user_id
        sql_util = SQLUtil(session=db_session)
        data = sql_util.fetch_as_json(
            self.expense_queries.get_expense_query(user_id=self.user_id,
                                                   expense_id=update_payload.expense_id,
                                                   category_id=update_payload.category_id))
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Category Id not found")
        query_dict = {"user_id": self.user_id, "expense_id":update_payload.expense_id, "category_id":update_payload.category_id}
        sql_util.update_postgres_columns(filter_dict=query_dict,
                                         update_dict=update_payload.model_dump(),
                                         table=TransactionOrmSchema)
        return DefaultResponse(message="Category Updated Successfully")

    def delete_existing_expense(self, db_session: Session, expense_id: str, category_id:str):
        sql_util = SQLUtil(session=db_session)
        sql_util.delete_data({"user_id": self.user_id,"expense_id": expense_id,
                              "category_id":category_id}, table=TransactionOrmSchema)
        return DefaultResponse(message="Category deleted successfully")
