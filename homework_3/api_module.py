import csv
import logging
import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from validators import validate_user_full_name, validate_enum, validate_account_number
from db import db_connection

logging.basicConfig(level=logging.INFO, filename='bank_api.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')


@db_connection
def add_users(cursor, *users):
    """
    Add one or many users to the DB. Each user must include 'user_full_name' and 'accounts'.
    """
    added = 0
    for user in users:
        try:
            if isinstance(user, list):
                for u in user:
                    name, surname = validate_user_full_name(u['user_full_name'])
                    cursor.execute('INSERT INTO User (name, surname, birth_day, accounts) VALUES (?, ?, ?, ?)',
                                   (name, surname, u.get('birth_day'), u['accounts']))
                    added += 1
            else:
                name, surname = validate_user_full_name(user['user_full_name'])
                cursor.execute('INSERT INTO User (name, surname, birth_day, accounts) VALUES (?, ?, ?, ?)',
                               (name, surname, user.get('birth_day'), user['accounts']))
                added += 1
        except Exception as e:
            logging.error(f"Failed to add user {user}: {e}")
            return f"Error adding users: {e}"

    logging.info(f"Successfully added {added} user(s)")
    return f"Successfully added {added} user(s)"


@db_connection
def add_banks(cursor, *banks):
    """
    Add one or many banks to the DB.
    """
    added = 0
    for bank in banks:
        try:
            if isinstance(bank, list):
                for b in bank:
                    cursor.execute('INSERT INTO Bank (name) VALUES (?)', (b['name'],))
                    added += 1
            else:
                cursor.execute('INSERT INTO Bank (name) VALUES (?)', (bank['name'],))
                added += 1
        except Exception as e:
            logging.error(f"Failed to add bank {bank}: {e}")
            return f"Error adding banks: {e}"

    logging.info(f"Successfully added {added} bank(s)")
    return f"Successfully added {added} bank(s)"


@db_connection
def add_accounts(cursor, *accounts):
    """
    Add one or many accounts to the DB.
    Fields: user_id, type, account_num, bank_id, currency, amount, status
    """
    allowed_statuses = ['active', 'inactive']
    allowed_types = ['debit', 'credit']
    allowed_currencies = ['USD', 'EUR', 'GBP']

    added = 0
    for acc in accounts:
        try:
            if isinstance(acc, list):
                for a in acc:
                    _insert_account(cursor, a, allowed_statuses, allowed_types, allowed_currencies)
                    added += 1
            else:
                _insert_account(cursor, acc, allowed_statuses, allowed_types, allowed_currencies)
                added += 1
        except Exception as e:
            logging.error(f"Failed to add account {acc}: {e}")
            return f"Error adding accounts: {e}"

    logging.info(f"Successfully added {added} account(s)")
    return f"Successfully added {added} account(s)"


def _insert_account(cursor, acc, statuses, types, currencies):
    validate_enum("status", acc['status'], statuses)
    validate_enum("type", acc['type'], types)
    validate_enum("currency", acc['currency'], currencies)
    cleaned_num = validate_account_number(acc['account_num'])

    cursor.execute('''INSERT INTO Account
        (user_id, type, account_num, bank_id, currency, amount, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (acc['user_id'], acc['type'], cleaned_num, acc['bank_id'],
                    acc['currency'], acc['amount'], acc['status']))


def add_users_from_csv(path):
    """
    Add users from a CSV file. Expects columns: user_full_name, birth_day, accounts
    """
    if not os.path.exists(path):
        return f"File {path} not found!"

    users = []
    try:
        with open(path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                users.append({
                    'user_full_name': row['user_full_name'],
                    'birth_day': row.get('birth_day'),
                    'accounts': row['accounts']
                })
        return add_users(users)
    except Exception as e:
        logging.error(f"Failed to add users from CSV: {e}")
        return f"Error reading user CSV: {e}"


def add_banks_from_csv(path):
    """
    Add banks from a CSV file. Expects column: name
    """
    if not os.path.exists(path):
        return f"File {path} not found!"

    banks = []
    try:
        with open(path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                banks.append({'name': row['name']})
        return add_banks(banks)
    except Exception as e:
        logging.error(f"Failed to add banks from CSV: {e}")
        return f"Error reading bank CSV: {e}"


def add_accounts_from_csv(path):
    """
    Add accounts from a CSV file.
    Expects columns: user_id, type, account_num, bank_id, currency, amount, status
    """
    if not os.path.exists(path):
        return f"File {path} not found!"

    accounts = []
    try:
        with open(path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                accounts.append({
                    'user_id': int(row['user_id']),
                    'type': row['type'],
                    'account_num': row['account_num'],
                    'bank_id': int(row['bank_id']),
                    'currency': row['currency'],
                    'amount': float(row['amount']),
                    'status': row['status']
                })
        return add_accounts(accounts)
    except Exception as e:
        logging.error(f"Failed to add accounts from CSV: {e}")
        return f"Error reading account CSV: {e}"


@db_connection
def modify_user(cursor, user_id, new_name=None, new_surname=None, new_birth_day=None, new_accounts=None):
    try:
        set_values = []
        if new_name:
            set_values.append(f"name = '{new_name}'")
        if new_surname:
            set_values.append(f"surname = '{new_surname}'")
        if new_birth_day:
            set_values.append(f"birth_day = '{new_birth_day}'")
        if new_accounts:
            set_values.append(f"accounts = '{new_accounts}'")

        if not set_values:
            return "No data provided to modify."

        query = f"UPDATE User SET {', '.join(set_values)} WHERE id = {user_id}"
        cursor.execute(query)
        return f"User {user_id} successfully updated."
    except Exception as e:
        logging.error(f"Error modifying user {user_id}: {e}")
        return f"Failed to modify user {user_id}: {e}"


@db_connection
def modify_bank(cursor, bank_id, new_name):
    try:
        query = f"UPDATE Bank SET name = '{new_name}' WHERE id = {bank_id}"
        cursor.execute(query)
        return f"Bank {bank_id} successfully updated."
    except Exception as e:
        logging.error(f"Error modifying bank {bank_id}: {e}")
        return f"Failed to modify bank {bank_id}: {e}"


@db_connection
def modify_account(cursor, account_id, new_type=None, new_account_num=None, new_currency=None, new_amount=None,
                   new_status=None):
    try:
        set_values = []
        if new_type:
            set_values.append(f"type = '{new_type}'")
        if new_account_num:
            set_values.append(f"account_num = '{new_account_num}'")
        if new_currency:
            set_values.append(f"currency = '{new_currency}'")
        if new_amount:
            set_values.append(f"amount = {new_amount}")
        if new_status:
            set_values.append(f"status = '{new_status}'")

        if not set_values:
            return "No data provided to modify."

        query = f"UPDATE Account SET {', '.join(set_values)} WHERE id = {account_id}"
        cursor.execute(query)
        return f"Account {account_id} successfully updated."
    except Exception as e:
        logging.error(f"Error modifying account {account_id}: {e}")
        return f"Failed to modify account {account_id}: {e}"


@db_connection
def delete_user(cursor, user_id):
    try:
        cursor.execute(f"DELETE FROM User WHERE id = {user_id}")
        return f"User {user_id} successfully deleted."
    except Exception as e:
        logging.error(f"Error deleting user {user_id}: {e}")
        return f"Failed to delete user {user_id}: {e}"


@db_connection
def delete_bank(cursor, bank_id):
    try:
        cursor.execute(f"DELETE FROM Bank WHERE id = {bank_id}")
        return f"Bank {bank_id} successfully deleted."
    except Exception as e:
        logging.error(f"Error deleting bank {bank_id}: {e}")
        return f"Failed to delete bank {bank_id}: {e}"


@db_connection
def delete_account(cursor, account_id):
    try:
        cursor.execute(f"DELETE FROM Account WHERE id = {account_id}")
        return f"Account {account_id} successfully deleted."
    except Exception as e:
        logging.error(f"Error deleting account {account_id}: {e}")
        return f"Failed to delete account {account_id}: {e}"


@db_connection
def transfer_money(cursor, sender_account_id, receiver_account_id, amount, transaction_datetime=None):
    """
    :param cursor: SQLite database connection.
    :param sender_account_id: ID of the sender's account.
    :param receiver_account_id: ID of the receiver's account.
    :param amount: Amount of money to transfer.
    :param transaction_datetime: Date and time of the transaction. If not provided, the current time will be used.
    :return: A message indicating the success or failure of the transaction.
    """
    try:
        cursor.execute("SELECT amount, currency, bank_id FROM Account WHERE id = ?", (sender_account_id,))
        sender = cursor.fetchone()
        if not sender:
            return f"Sender account {sender_account_id} not found."

        sender_balance, sender_currency, sender_bank_id = sender

        if sender_balance < amount:
            return f"Sender account {sender_account_id} has insufficient balance."

        cursor.execute("SELECT name FROM Bank WHERE id = ?", (sender_bank_id,))
        sender_bank = cursor.fetchone()
        if not sender_bank:
            return f"Sender's bank with id {sender_bank_id} not found."
        sender_bank_name = sender_bank[0]

        cursor.execute("SELECT amount, currency, bank_id FROM Account WHERE id = ?", (receiver_account_id,))
        receiver = cursor.fetchone()
        if not receiver:
            return f"Receiver account {receiver_account_id} not found."

        receiver_balance, receiver_currency, receiver_bank_id = receiver

        if sender_currency != receiver_currency:
            exchange_rate = get_exchange_rate(sender_currency, receiver_currency)
            if not exchange_rate:
                return "Failed to retrieve exchange rate."
            amount_in_receiver_currency = amount * exchange_rate
        else:
            amount_in_receiver_currency = amount

        new_sender_balance = sender_balance - amount
        cursor.execute("UPDATE Account SET amount = ? WHERE id = ?", (new_sender_balance, sender_account_id))

        new_receiver_balance = receiver_balance + amount_in_receiver_currency
        cursor.execute("UPDATE Account SET amount = ? WHERE id = ?", (new_receiver_balance, receiver_account_id))

        cursor.execute("SELECT name FROM Bank WHERE id = ?", (receiver_bank_id,))
        receiver_bank = cursor.fetchone()
        if not receiver_bank:
            return f"Receiver's bank with id {receiver_bank_id} not found."
        receiver_bank_name = receiver_bank[0]

        transaction_datetime = transaction_datetime or datetime.now()

        transaction_query = """
            INSERT INTO Transactions (account_sender_id, account_receiver_id, sent_currency, sent_amount, 
            bank_sender_name, bank_receiver_name, datetime)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(transaction_query, (sender_account_id, receiver_account_id, sender_currency,
                                           amount, sender_bank_name,
                                           receiver_bank_name, transaction_datetime))

        return f"Successfully transferred {amount} {sender_currency} from account {sender_account_id} to {receiver_account_id}."

    except Exception as e:
        logging.error(f"Error in money transfer: {e}")
        return f"Failed to transfer money: {e}"


def get_exchange_rate(from_currency, to_currency):
    """
    Fetch exchange rate from external API.
    """
    try:
        load_dotenv()
        api_key = os.getenv(key='API_KEY')
        url = (f'https://api.freecurrencyapi.com/v1/latest?apikey={api_key}&base_currency={from_currency}'
               f'&currencies={to_currency}')
        response = requests.get(url)
        data = response.json()

        if 'data' in data and to_currency in data['data']:
            return data['data'][to_currency]
        else:
            return None
    except Exception as e:
        logging.error(f"Error fetching exchange rate: {e}")
        return None
