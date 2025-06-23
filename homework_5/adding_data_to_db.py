import logging
import csv
from homework_5.db_connection_decorator import db_connection
from homework_5.consts import (LOGGER_NAME, ALLOWED_STATUSES, ALLOWED_TYPES, SQL_INSERT_USER, SQL_INSERT_BANK,
                               SQL_INSERT_ACCOUNT)
from homework_5.validate_data import validate_user_name, validate_fields, validate_account_number


@db_connection
def add_users(*args, cursor=None):
    """
    description:
    connect with db, transform user data into SQL INSERT commands and execute them

    :param args: list of user dictionaries or nested lists of user dictionaries.
                 each dictionary must contain 'user_fullname' and 'birth_day'
    :param cursor: db connection cursor (auto-injected by @db_connection)

    :return: --> str (success message) or Exception (if error occurs)
    """
    logger = logging.getLogger(LOGGER_NAME)

    def process(data):
        for user in data:
            if isinstance(user, list):
                process(user)
            else:
                full_name = user['user_fullname']
                birth_day = user['birth_day']
                name, surname = validate_user_name(full_name)
                cursor.execute(SQL_INSERT_USER, (name, surname, birth_day))

    try:
        process(args)
    except Exception as e:
        logger.error(e)
        return e

    logger.info('Successfully added user(s)')
    return 'Successfully added user(s)'


@db_connection
def add_banks(*args, cursor=None):
    """
    description:
    connect with db, transform bank data into SQL INSERT commands and execute them

    :param args: list of bank dictionaries or nested lists of dictionaries.
                 each dictionary must contain 'bank_name'
    :param cursor: db connection cursor (auto-injected by @db_connection)

    :return: --> str (success message) or Exception (if error occurs)
    """
    logger = logging.getLogger(LOGGER_NAME)

    def process(data):
        for bank in data:
            if isinstance(bank, list):
                process(bank)
            else:
                bank_name = bank['bank_name']
                cursor.execute(SQL_INSERT_BANK, (bank_name,))
    try:
        process(args)
    except Exception as e:
        logger.error(e)
        return e

    logger.info("Bank(s) successfully added to database")
    return "Bank(s) successfully added to database"


@db_connection
def add_accounts(*args, cursor=None):
    """
    description:
    connect with db, validate and transform account data into SQL INSERT commands and execute them

    :param args: list of account dictionaries or nested lists of dictionaries.
    each dictionary must contain 'user_id', 'type', 'account_num', 'bank_id', 'currency', 'amount', 'status'
    :param cursor: db connection cursor (auto-injected by @db_connection)

    :return: --> str (success message) or False (if error occurs)
    """
    logger = logging.getLogger(LOGGER_NAME)

    def process(data):
        try:
            for account in data:
                if isinstance(account, list):
                    process(account)
                else:
                    try:
                        validate_fields('status', account['status'], ALLOWED_STATUSES)
                        validate_fields('type', account['type'], ALLOWED_TYPES)

                        account_num = validate_account_number(account['account_num'])
                        user_id = account['user_id']
                        type_card = account['type']
                        bank_id = account['bank_id']
                        currency = account['currency']
                        amount = account['amount']
                        status = account['status']
                        cursor.execute(SQL_INSERT_ACCOUNT,
                                       (int(user_id), type_card, account_num,
                                        int(bank_id), currency,
                                        float(amount),
                                        status))
                    except ValueError as e:
                        logger.warning(e)
            return True
        except Exception as e:
            logger.error(e)
            return False

    if process(args):
        logger.info('Successfully added account(s)')
        return 'Successfully added account(s)'


def add_data_from_csv(path: str, handler_func):
    """
    description:
    read data from CSV file and process each row using the given handler function

    :param path: path to CSV file
    :param handler_func: function to handle each row (must accept a single dictionary as argument)

    :return: --> void or Exception (if file not found)
    """
    logger = logging.getLogger(LOGGER_NAME)
    try:
        with open(path, mode='r', encoding='utf-8') as file:
            csv_reader = list(csv.DictReader(file))

            for data in csv_reader:
                handler_func(data)

        logger.info('Data from CSV file successfully added')
        return 'Data from CSV file successfully added'
    except FileNotFoundError as e:
        logger.error(e)
        return e
