import random
import logging
from db import db_connection


@db_connection
def generate_random_discounts(cursor, max_users=10):
    """
    Randomly selects users from the database and assigns them a random discount.
    The discount can be 25, 30, or 50.

    :param cursor: SQLite database connection
    :param max_users: Maximum number of users to select (default is 10)
    :return: Dictionary with user IDs and their corresponding discounts.
    """
    try:
        cursor.execute("SELECT id FROM User")
        users = cursor.fetchall()
        selected_users = random.sample(users, min(len(users), max_users))

        discounts = {user[0]: random.choice([25, 30, 50]) for user in selected_users}
        return discounts
    except Exception as e:
        logging.error(f"Error in generate_random_discounts: {e}")
        return {}


@db_connection
def get_users_with_debts(cursor):
    """
    Returns a list of users who have debts (negative account balances).

    :param cursor: SQLite database connection
    :return: List of full names of users with debts.
    """
    try:
        cursor.execute("SELECT u.id, u.name, u.surname, a.amount "
                       "FROM User u JOIN Account a ON u.id = a.user_id "
                       "WHERE a.amount < 0")
        debts = cursor.fetchall()
        return [(user[1] + " " + user[2]) for user in debts]
    except Exception as e:
        logging.error(f"Error in get_users_with_debts: {e}")
        return []


@db_connection
def get_bank_with_largest_capital(cursor):
    """
    Returns the bank with the largest capital (based on the sum of account balances).

    :param cursor: SQLite database connection
    :return: Bank ID with the largest capital or None if error occurs.
    """
    try:
        cursor.execute("SELECT bank_id, SUM(amount) FROM Account GROUP BY bank_id ORDER BY SUM(amount) DESC LIMIT 1")
        result = cursor.fetchone()
        return result
    except Exception as e:
        logging.error(f"Error in get_bank_with_largest_capital: {e}")
        return None


@db_connection
def get_bank_with_oldest_client(cursor):
    """
    Returns the bank that serves the oldest client (based on the earliest birth date).

    :param cursor: SQLite database connection
    :return: Tuple (bank_name, birth_day) or None if error occurs.
    """
    try:
        cursor.execute("""
            SELECT b.name, MIN(u.birth_day)
            FROM User u
            JOIN Account a ON u.id = a.user_id
            JOIN Bank b ON a.bank_id = b.id
            GROUP BY b.id
            ORDER BY MIN(u.birth_day)
            LIMIT 1
        """)
        result = cursor.fetchone()
        return result
    except Exception as e:
        logging.error(f"Error in get_bank_with_oldest_client: {e}")
        return None


@db_connection
def get_highest_number_of_unique_user_bank(cursor):
    """
    Checks each transaction for unique users, then associates them with a bank.
    Counts the number of unique users for each bank and returns the bank with the highest number of unique users.

    :param cursor: SQLite database connection
    :return: Name of the bank with the highest number of unique users, or None if error occurs.
    """
    try:
        cursor.execute("SELECT bank_sender_name, account_sender_id FROM Transactions")
        transactions = cursor.fetchall()

        bank_and_users_id = {}

        for transaction in transactions:
            sender_bank = transaction[0]
            sender_user_id = transaction[1]

            if sender_bank in bank_and_users_id:
                bank_and_users_id[sender_bank].add(sender_user_id)
            else:
                bank_and_users_id[sender_bank] = {sender_user_id}

        highest_bank = max(bank_and_users_id, key=lambda bank_key: len(bank_and_users_id[bank_key]))

        return highest_bank
    except Exception as e:
        logging.error(f"Error in get_highest_number_of_unique_user_bank: {e}")
        return None


@db_connection
def delete_incomplete_users_and_accounts(cursor):
    """
    Deletes incomplete user and account records from the database.
    If mandatory data is missing for a user or account, the records will be deleted.

    :param cursor: SQLite database connection
    """
    try:
        cursor.execute("""
            DELETE FROM User
            WHERE name IS NULL OR surname IS NULL OR accounts IS NULL
        """)

        cursor.execute("""
            DELETE FROM Account
            WHERE account_num IS NULL OR user_id IS NULL OR amount IS NULL
        """)

        logging.info("Deleted incomplete users and accounts.")
    except Exception as e:
        logging.error(f"Error deleting incomplete users and accounts: {e}")
        cursor.connection.rollback()


@db_connection
def get_user_transactions_last_3_months(cursor, user_id):
    """
    Fetches transactions for a particular user within the past 3 months.

    :param cursor: SQLite database connection
    :param user_id: ID of the user whose transactions to fetch
    :return: List of transactions in the last 3 months as a list of dictionaries.
    """
    try:
        cursor.execute("""
            SELECT
                t.id AS transaction_id,
                t.bank_sender_name AS sender_bank,
                t.account_sender_id AS sender_account_id,
                t.bank_receiver_name AS receiver_bank,
                t.account_receiver_id AS receiver_account_id,
                t.sent_currency AS currency,
                t.sent_amount AS amount,
                t.datetime AS transaction_date
            FROM Transactions t
            WHERE t.datetime >= date('now', '-3 months')
            AND (t.account_sender_id = ? OR t.account_receiver_id = ?)
        """, (user_id, user_id))

        rows = cursor.fetchall()

        columns = [description[0] for description in cursor.description]
        transactions = [dict(zip(columns, row)) for row in rows]

        return transactions

    except Exception as e:
        logging.error(f"Error in get_user_transactions_last_3_months: {e}")
        return []
