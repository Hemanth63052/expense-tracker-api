from sqlalchemy import select, and_
from scripts.db.sql_table_orm_schemas import CategoriesOrmSchema

class CategoryQueries:

    @staticmethod
    def get_category_query(user_id, category_id=None, title: str = None):
        where_conditions = [CategoriesOrmSchema.user_id == user_id]
        if category_id:
            where_conditions.append(CategoriesOrmSchema.category_id == category_id)
        if title:
            where_conditions.append(CategoriesOrmSchema.title == title)
        return select(CategoriesOrmSchema.category_id.label("value"),
                      CategoriesOrmSchema.title.label("label"),
                      CategoriesOrmSchema.description).where(and_(*where_conditions))

