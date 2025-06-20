import logging
from homework_4.db_connection_decorator import db_connection
from homework_4.consts import (LOGGER_NAME, SQL_UPDATE_USER_FIELD, SQL_UPDATE_BANK_FIELD, SQL_UPDATE_ACCOUNT_FIELD,
                               ALLOWED_STATUSES, ALLOWED_TYPES)
from typing import Any
from homework_4.validate_data import validate_account_number, validate_fields


@db_connection
def modify_user(user_id: int, variable: str, new_data: Any, cursor=None):
    """
    description:
    connect with db and update a specific field of a user by user_id

    :param user_id: id of the user to update
    :param variable: name of the field to update ('name', 'surname', 'birth_day', 'accounts')
    :param new_data: new value to set for the field
    :param cursor: db connection cursor (auto-injected by @db_connection)

    :return: --> str (success message) or Exception (if error occurs)
    """
    logger = logging.getLogger(LOGGER_NAME)
    try:
        allowed_fields = ['name', 'surname', 'birth_day', 'accounts']
        if variable not in allowed_fields:
            raise ValueError('There is no such attribute in the table.')

        query = SQL_UPDATE_USER_FIELD.format(variable)
        cursor.execute(query, (new_data, user_id))

        logger.info(f'Successfully changed field {variable} in table User')
        return f'Successfully changed field {variable} in table User'
    except Exception as e:
        logger.error(e)
        return e


@db_connection
def modify_bank(bank_id: int, variable: str, new_data: Any, cursor=None):
    """
    description:
    update a specific field of a bank record by bank_id in the database

    :param bank_id: id of the bank to update
    :param variable: name of the field to update ('name')
    :param new_data: new value to set for the field
    :param cursor: db connection cursor (optional, for internal use)

    :return: --> str (success message) or Exception (if error occurs)
    """
    logger = logging.getLogger(LOGGER_NAME)
    try:
        allowed_fields = ['name']
        if variable not in allowed_fields:
            raise ValueError('There is no such attribute in the table.')

        query = SQL_UPDATE_BANK_FIELD.format(variable)
        cursor.execute(query, (new_data, bank_id))

        logger.info(f'Successfully changed field {variable} in table Bank')
        return f'Successfully changed field {variable} in table Bank'
    except Exception as e:
        logger.error(e)
        return e


@db_connection
def modify_account(account_id: int, variable: str, new_data: Any, cursor=None):
    """
    description:
    update a specific field of an account record by account_id in the database

    :param account_id: id of the account to update
    :param variable: name of the field to update (one of ['account_num', 'user_id', 'type', 'bank_id', 'currency',
    'amount', 'status'])
    :param new_data: new value to set for the field
    :param cursor: db connection cursor (auto-injected by @db_connection)

    :return: --> str (success message) or Exception (if error occurs)
    """
    logger = logging.getLogger(LOGGER_NAME)
    try:
        allowed_fields = ['account_num', 'user_id', 'type', 'bank_id', 'currency', 'amount', 'status']
        if variable not in allowed_fields:
            raise ValueError('There is no such attribute in the table.')

        if variable == 'account_num':
            new_data = validate_account_number(new_data)
        elif variable in ('status', 'type'):
            validate_fields(variable, new_data, ALLOWED_STATUSES if variable == 'status' else ALLOWED_TYPES)

        query = SQL_UPDATE_ACCOUNT_FIELD.format(variable)
        cursor.execute(query, (new_data, account_id))

        logger.info(f'Successfully changed field {variable} in table Account')
        return f'Successfully changed field {variable} in table Account'
    except Exception as e:
        logger.error(e)
        return e
