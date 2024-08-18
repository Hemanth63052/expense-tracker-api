from sqlalchemy import select, and_
from scripts.db.sql_table_orm_schemas import TransactionOrmSchema

class ExpenseQueries:

    @staticmethod
    def get_expense_query(user_id, expense_id=None, category_id: str = None,
                          expense_name: str = None):
        where_conditions = [TransactionOrmSchema.user_id == user_id]
        if expense_id:
            where_conditions.append(TransactionOrmSchema.expense_id == expense_id)
        if category_id:
            where_conditions.append(TransactionOrmSchema.category_id.in_([category_id]))
        if expense_name:
            where_conditions.append(TransactionOrmSchema.expense_name == expense_name)
        return select(TransactionOrmSchema.expense_id.label("value"),
                       TransactionOrmSchema.expense_name.label("label"),
                       TransactionOrmSchema.note).where(and_(*where_conditions))

