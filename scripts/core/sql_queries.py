from scripts.db.sql_table_orm_schemas import UserDetailsOrmSchema
from sqlalchemy import select


class SQLQueries:

    @staticmethod
    def get_user_details_by_email(email):
        """
        Get user details by email.
        :param email:
        :return:
        """
        return select(*UserDetailsOrmSchema.__table__.columns).where(
            UserDetailsOrmSchema.email == email
        )

    @staticmethod
    def get_details_by_user_id(user_id):
        """
        Get user details by user id.
        :param user_id:
        :return:
        """
        return select(*UserDetailsOrmSchema.__table__.columns).where(
            UserDetailsOrmSchema.user_id == user_id
        )
