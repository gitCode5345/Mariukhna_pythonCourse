import sqlite3


def db_connection(func):
    """
    description:
    open SQLite connection, enable foreign keys, execute target function with db cursor, commit and close connection

    :param func: target function that requires a database cursor (injected as keyword argument)

    :return: --> wrapped function with automatic db connection handling
    """
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('bank_data.db', timeout=10)
        cursor = conn.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        try:
            return func(*args, **kwargs, cursor=cursor)
        finally:
            conn.commit()
            cursor.close()
            conn.close()

    return wrapper
