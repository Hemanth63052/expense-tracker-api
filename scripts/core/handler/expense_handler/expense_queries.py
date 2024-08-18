from scripts.db.sql_table_orm_schemas import TransactionOrmSchema
from sqlalchemy import and_, select


class ExpenseQueries:

    @staticmethod
    def get_expense_query(
        user_id, expense_id=None, category_id: str = None, expense_name: str = None
    ):
        """
        Retrieve the query for expense list for a specific user.
        Args:
            user_id (str): The id of the user.
            expense_id (str): The id of the expense.
            category_id (str): The id of the category.
            expense_name (str): The name of the expense.
        :returns
            select: The query for expense list for a specific user.
        """
        where_conditions = [TransactionOrmSchema.user_id == user_id]
        if expense_id:
            where_conditions.append(TransactionOrmSchema.expense_id == expense_id)
        if category_id:
            where_conditions.append(TransactionOrmSchema.category_id.in_([category_id]))
        if expense_name:
            where_conditions.append(TransactionOrmSchema.expense_name == expense_name)
        return select(
            TransactionOrmSchema.expense_id.label("value"),
            TransactionOrmSchema.expense_name.label("label"),
            TransactionOrmSchema.note,
        ).where(and_(*where_conditions))
