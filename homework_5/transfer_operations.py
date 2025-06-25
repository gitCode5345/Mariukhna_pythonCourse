import logging
import os
from datetime import datetime
import requests
from dotenv import load_dotenv
from homework_5.db_connection_decorator import db_connection
from homework_5.consts import (LOGGER_NAME, SQL_SELECT_ACCOUNT_INFO, SQL_UPDATE_ACCOUNT_AFTER_TRANSACTION,
                               SQL_SELECT_BANK_NAME, SQL_INSERT_TRANSACTION)


@db_connection
def send_money(sender_account_id: int, receiver_account_id: int, amount: float, transaction_date=None, cursor=None):
    """
    description:
    perform a money transfer between two accounts with currency conversion if needed,
    update balances, and log the transaction

    :param sender_account_id: id of the sender's account
    :param receiver_account_id: id of the receiver's account
    :param amount: amount of money to send (in sender's currency)
    :param transaction_date: date and time of the transaction, if this parameter is not specified, the time will be
    added automatically
    :param cursor: db connection cursor (auto-injected by @db_connection)

    :return: --> None or error message string if insufficient funds or exception occurs
    """
    logger = logging.getLogger(LOGGER_NAME)
    try:
        if amount <= 0:
            raise ValueError('Invalid value for funds transfer')

        sender_response = cursor.execute(SQL_SELECT_ACCOUNT_INFO, (sender_account_id,)).fetchone()

        sender_amount = sender_response[0]
        sender_currency = sender_response[1]
        sender_bank_id = sender_response[2]

        if sender_amount < amount:
            logger.warning('There are not enough funds to send to make the transfer.')
            return 'There are not enough funds to send to make the transfer.'

        receiver_response = cursor.execute(SQL_SELECT_ACCOUNT_INFO, (receiver_account_id,)).fetchone()

        receiver_amount = receiver_response[0]
        receiver_currency = receiver_response[1]
        receiver_bank_id = receiver_response[2]

        before_amount = amount
        if receiver_currency != sender_currency:
            amount = convert_currency(sender_currency, receiver_currency, amount)
            sender_amount = sender_amount - before_amount
        else:
            sender_amount = sender_amount - amount
        receiver_amount = receiver_amount + amount

        cursor.execute(SQL_UPDATE_ACCOUNT_AFTER_TRANSACTION, (float(sender_amount), int(sender_account_id)))
        cursor.execute(SQL_UPDATE_ACCOUNT_AFTER_TRANSACTION, (float(receiver_amount), int(receiver_account_id)))

        sender_bank_name = cursor.execute(SQL_SELECT_BANK_NAME, (sender_bank_id,)).fetchone()
        receiver_bank_name = cursor.execute(SQL_SELECT_BANK_NAME, (receiver_bank_id,)).fetchone()

        if transaction_date is None:
            transaction_date = datetime.now().strftime('%Y-%m-%d %H:%M')
        cursor.execute(SQL_INSERT_TRANSACTION,
                       (sender_bank_name[0], int(sender_account_id), receiver_bank_name[0],
                        int(receiver_account_id), sender_currency, int(before_amount)
                        if receiver_currency != sender_currency else int(amount), transaction_date))

        logger.info('Transaction from ID %s to ID %s completed successfully.',
                    sender_account_id, receiver_account_id)
        return f'Transaction from ID {sender_account_id} to ID {receiver_account_id} completed successfully.'
    except Exception as e:
        logger.error(e)
        return e


def convert_currency(from_currency: str, to_currency: str, amount: float):
    """
    description:
    convert a monetary amount from one currency to another using an external currency API

    :param from_currency: source currency code (e.g., 'USD')
    :param to_currency: target currency code (e.g., 'EUR')
    :param amount: amount in source currency to convert

    :return: --> float (converted amount) or raises ValueError on API error or limit exceeded
    """
    load_dotenv()
    key = os.getenv('API_KEY')
    logger = logging.getLogger(LOGGER_NAME)

    response = requests.get(f'https://api.freecurrencyapi.com/v1/latest?apikey={key}', timeout=60)
    if response.status_code == 200:
        logger.info('Fetching data from the API to retrieve exchange rates.')

        data = response.json().get('data', [])
        value_from_currency = data[from_currency]
        value_to_currency = data[to_currency]

        return amount * (value_to_currency / value_from_currency)
    if response.status_code == 429:
        raise ValueError('Request limit reached.')

    raise ValueError('An error occurred while retrieving currency rates.')
