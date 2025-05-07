import sqlite3


def db_connection(func):
    """
    A decorator to establish a database connection before calling a function.
    """
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('bank_data.db')
        cursor = conn.cursor()
        try:
            return func(cursor, *args, **kwargs)
        finally:
            conn.commit()
            cursor.close()
            conn.close()

    return wrapper
