import logging
import random
from homework_4.db_connection_decorator import db_connection
from homework_4.consts import (DISCOUNTS, LOGGER_NAME, SQL_SELECT_RANDOM_ID_USER_WITH_LIMIT,
                               SQL_SELECT_USERS_WITH_DEBTS, SQL_SELECT_BANK_WITH_LARGEST_CAPITAL,
                               SQL_SELECT_BANK_SERVING_OLDEST_CLIENT, SQL_SELECT_BANK_WITH_MOST_OUTBOUND_USERS,
                               SQL_DELETE_USERS_WITHOUT_FULL_INFO, SQL_SELECT_TRANSACTIONS_LAST_3_MONTHS)


@db_connection
def get_random_credit_discount(cursor=None):
    """
    description:
    randomly select users from the database and assign each a random credit discount

    :param cursor: db connection cursor (auto-injected by @db_connection)

    :return: --> dict {user_id: discount} or Exception (if error occurs)
    """
    logger = logging.getLogger(LOGGER_NAME)
    logger.info('Start issuing random discounts to random users')
    try:
        number_of_discounts = random.randint(0, 10)
        query = SQL_SELECT_RANDOM_ID_USER_WITH_LIMIT.format(number_of_discounts)
        all_users_ids = cursor.execute(query).fetchall()

        result = {ids[0]: random.choice(DISCOUNTS) for ids in all_users_ids}
        logger.info('Discounts issued successfully')
        return result
    except Exception as e:
        logger.error(e)
        return e


@db_connection
def get_users_with_debts(cursor=None):
    """
    description:
    retrieve a list of users who have negative balances on at least one of their accounts

    :param cursor: db connection cursor (auto-injected by @db_connection)

    :return: --> list of tuples (name, surname) of users with debts
    """
    logger = logging.getLogger(LOGGER_NAME)
    logger.info('Finding users with debts')
    try:
        users = cursor.execute(SQL_SELECT_USERS_WITH_DEBTS).fetchall()
        logger.info('Information successfully found')
        return users
    except Exception as e:
        logger.error(e)
        return e


@db_connection
def get_bank_with_largest_capital(cursor=None):
    """
    description:
    retrieve the name of the bank with the largest total capital based on account balances

    :param cursor: db connection cursor (auto-injected by @db_connection)

    :return: --> tuple (bank_name) or None if no data
    """
    logger = logging.getLogger(LOGGER_NAME)
    logger.info('Collecting information about banks with the largest capital')
    try:
        bank = cursor.execute(SQL_SELECT_BANK_WITH_LARGEST_CAPITAL).fetchone()
        logger.info('Information successfully found')
        return bank
    except Exception as e:
        logger.error(e)
        return e


@db_connection
def get_bank_serving_oldest_client(cursor=None):
    """
    description:
    retrieve the name of the bank that serves the oldest client based on user's birthdate

    :param cursor: db connection cursor (auto-injected by @db_connection)

    :return: --> tuple (bank_name) or None if no data
    """
    logger = logging.getLogger(LOGGER_NAME)
    logger.info('Defining the most feared bank customer')
    try:
        bank = cursor.execute(SQL_SELECT_BANK_SERVING_OLDEST_CLIENT).fetchone()
        logger.info('Information successfully found')
        return bank
    except Exception as e:
        logger.error(e)
        return e


@db_connection
def get_bank_with_most_outbound_users(cursor=None):
    """
    description:
    retrieve the bank name with the highest number of unique users who sent transactions

    :param cursor: db connection cursor (auto-injected by @db_connection)

    :return: --> tuple (bank_name) or None if no data
    """
    logger = logging.getLogger(LOGGER_NAME)
    logger.info('Search for the bank with the highest number of outgoing transactions')
    try:
        bank = cursor.execute(SQL_SELECT_BANK_WITH_MOST_OUTBOUND_USERS).fetchone()
        logger.info('Information successfully found')
        return bank
    except Exception as e:
        logger.error(e)
        return e


@db_connection
def delete_users_without_full_info(cursor=None):
    """
    description:
    delete users from the database who have incomplete personal information
    (empty name, surname, or birthdate)

    :param cursor: db connection cursor (auto-injected by @db_connection)

    :return: --> str (success message)
    """
    logger = logging.getLogger(LOGGER_NAME)
    logger.info('Removing users with incomplete information')
    try:
        cursor.execute(SQL_DELETE_USERS_WITHOUT_FULL_INFO)
        logger.info('Successfully removed users with incomplete information')
        return 'Successfully removed users with incomplete information'
    except Exception as e:
        logger.error(e)
        return e


@db_connection
def get_transactions_last_3_months(user_id: int, cursor=None):
    """
    description:
    retrieve all transactions involving the user’s accounts from the last 3 months

    :param user_id: id of the user whose transactions to fetch
    :param cursor: db connection cursor (auto-injected by @db_connection)

    :return: --> list of transactions (rows) or empty list if none found
    """
    logger = logging.getLogger(LOGGER_NAME)
    logger.info(f'Getting user transactions with id {user_id} for the last 3 months')

    try:
        query = SQL_SELECT_TRANSACTIONS_LAST_3_MONTHS.format(user_id, user_id)
        transactions = cursor.execute(query).fetchall()
        logger.info('Information successfully found')
        return transactions
    except Exception as e:
        logger.error(e)
        return e
