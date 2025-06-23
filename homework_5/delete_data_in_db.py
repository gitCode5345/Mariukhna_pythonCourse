import logging
from homework_5.consts import LOGGER_NAME
from homework_5.db_connection_decorator import db_connection


@db_connection
def delete_user(user_id: int, cursor=None):
    """
    description:
    delete a user record from the database by user_id

    :param user_id: id of the user to delete
    :param cursor: db connection cursor (auto-injected by @db_connection)

    :return: --> None or Exception (if error occurs)
    """
    logger = logging.getLogger(LOGGER_NAME)
    try:
        cursor.execute('DELETE FROM User WHERE id = ?', (user_id,))
        logger.info('Successfully deleted user with id %s', user_id)
        return f'Successfully deleted user with id {user_id}'
    except Exception as e:
        logger.error(e)
        return e


@db_connection
def delete_bank(bank_id: int, cursor=None):
    """
    description:
    delete a bank record from the database by bank_id

    :param bank_id: id of the bank to delete
    :param cursor: db connection cursor (auto-injected by @db_connection)

    :return: --> str (success message) or Exception (if error occurs)
    """
    logger = logging.getLogger(LOGGER_NAME)
    try:
        cursor.execute('DELETE FROM Bank WHERE id = ?', (bank_id,))
        logger.info('Successfully deleted bank with id %s', bank_id)
        return f'Successfully deleted bank with id {bank_id}'
    except Exception as e:
        logger.error(e)
        return e


@db_connection
def delete_account(account_id: int, cursor=None):
    """
    description:
    delete an account record from the database by account_id

    :param account_id: id of the account to delete
    :param cursor: db connection cursor (auto-injected by @db_connection)

    :return: --> str (success message) or Exception (if error occurs)
    """
    logger = logging.getLogger(LOGGER_NAME)
    try:
        cursor.execute('DELETE FROM Account WHERE id = ?', (account_id,))
        logger.info('Successfully deleted account with id %s', account_id)
        return f'Successfully deleted account with id {account_id}'
    except Exception as e:
        logger.error(e)
        return e
