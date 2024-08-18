from scripts.db.sql_table_orm_schemas import CategoriesOrmSchema
from sqlalchemy import and_, select


class CategoryQueries:

    @staticmethod
    def get_category_query(user_id, category_id=None, title: str = None):
        """
         Retrieve the query for category list for a specific user.
         Args:
             user_id (str): The id of the user.
             category_id (str): The id of the category.
             title (str): The title of the category.
        :returns
            select: The query for category list for a specific user.
        """
        where_conditions = [CategoriesOrmSchema.user_id == user_id]
        if category_id:
            where_conditions.append(CategoriesOrmSchema.category_id == category_id)
        if title:
            where_conditions.append(CategoriesOrmSchema.title == title)
        return select(
            CategoriesOrmSchema.category_id.label("value"),
            CategoriesOrmSchema.title.label("label"),
            CategoriesOrmSchema.description,
        ).where(and_(*where_conditions))
