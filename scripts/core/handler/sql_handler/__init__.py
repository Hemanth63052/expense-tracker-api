from scripts.utils.session_util import SessionUtil


def get_db_session(database="expense_tracker"):
    return SessionUtil().get_session(database=database)
