from scripts.utils.session_util import SessionUtil


def get_db_session(database="expense_tracker"):
    """
    Get the database session.
    :param database:
    :returns:
        Session: The database session.
    """
    return SessionUtil().get_session(database=database)
