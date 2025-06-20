import pytest
import os
import tempfile
import sqlite3
from unittest.mock import MagicMock, patch
from homework_4.consts import (SQL_CREATE_TABLE_USER_FOR_TEST, SQL_CREATE_TABLE_BANK_FOR_TEST,
                               SQL_CREATE_TABLE_ACCOUNT_FOR_TEST, SQL_CREATE_TABLE_TRANSACTIONS_FOR_TEST)


@pytest.fixture
def mock_db_cursor():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    with patch('sqlite3.connect', return_value=mock_conn):
        yield mock_cursor


@pytest.fixture
def valid_user_name():
    return 'John Test'


@pytest.fixture
def valid_account_num():
    return 'ID--jh-p-001273-xz'


@pytest.fixture
def valid_account_num_with_replace():
    return 'ID--jh-p-0#12#3-xz'


@pytest.fixture
def valid_account_type():
    return 'credit'


@pytest.fixture
def valid_status():
    return 'gold'


@pytest.fixture
def sample_csv_file():
    data = "name,surname\nJohn,Doe\nJane,Doe\n"
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.csv') as tmp:
        tmp.write(data)
        tmp_path = tmp.name
    yield tmp_path
    os.remove(tmp_path)


@pytest.fixture
def valid_allowed_statuses():
    return ['gold', 'silver', 'platinum']


@pytest.fixture
def valid_account_types():
    return ['credit', 'debit']


@pytest.fixture
def mock_convert_currency():
    with patch('homework_4.transfer_operations.convert_currency', return_value=100.0) as patched:
        yield patched


@pytest.fixture
def api_response():
    return {'data': {'USD': 1.0, 'EUR': 0.9}}


@pytest.fixture
def all_users_ids():
    return [(5,), (1,), (4,), (3,), (7,)]


@pytest.fixture
def mock_rand_int():
    with patch('random.randint', return_value=5) as patched:
        yield patched


@pytest.fixture
def mock_rand_choice():
    with patch('random.choice', side_effect=[25, 30, 50, 25, 30]) as patched:
        yield patched


@pytest.fixture
def mock_load_dotenv():
    with patch('homework_4.transfer_operations.load_dotenv') as patched:
        yield patched


@pytest.fixture
def mock_os_getenv():
    with patch('homework_4.transfer_operations.os.getenv') as patched:
        yield patched


@pytest.fixture
def mock_request_get():
    build_request = MagicMock()
    build_request.status_code = 200

    with patch('homework_4.transfer_operations.requests.get', return_value=build_request):
        yield build_request


def create_tables_for_db(cursor_db):
    cursor_db.execute(SQL_CREATE_TABLE_USER_FOR_TEST)
    cursor_db.execute(SQL_CREATE_TABLE_BANK_FOR_TEST)
    cursor_db.execute(SQL_CREATE_TABLE_ACCOUNT_FOR_TEST)
    cursor_db.execute(SQL_CREATE_TABLE_TRANSACTIONS_FOR_TEST)


def insert_general_test_data(cursor_db):
    cursor_db.execute("INSERT INTO Bank (name) VALUES ('PrivatBank')")
    cursor_db.execute("INSERT INTO Bank (name) VALUES ('MonoBank')")

    cursor_db.execute("SELECT id FROM Bank WHERE name = 'PrivatBank'")
    privat_id = cursor_db.fetchone()[0]
    cursor_db.execute("SELECT id FROM Bank WHERE name = 'MonoBank'")
    mono_id = cursor_db.fetchone()[0]

    cursor_db.execute("INSERT INTO User (name, surname, birth_day, accounts)\
                       VALUES ('Alice', 'Smith', '1990-01-01', '1,2')")
    cursor_db.execute("INSERT INTO User (name, surname, birth_day, accounts)\
                       VALUES ('Bob', 'Brown', '1985-05-05', '3')")
    cursor_db.execute("INSERT INTO User (name, surname)\
                           VALUES ('Bob', 'Brown')")

    cursor_db.execute("SELECT id FROM User WHERE name = 'Alice'")
    alice_id = cursor_db.fetchone()[0]
    cursor_db.execute("SELECT id FROM User WHERE name = 'Bob'")
    bob_id = cursor_db.fetchone()[0]

    cursor_db.execute("""
        INSERT INTO Account (user_id, type, account_num, bank_id, currency, amount, status)
        VALUES (?, 'debit', 'UA1234567890', ?, 'USD', 500.0, 'gold')
    """, (alice_id, privat_id))

    cursor_db.execute("""
        INSERT INTO Account (user_id, type, account_num, bank_id, currency, amount, status)
        VALUES (?, 'credit', 'UA9876543210', ?, 'EUR', -150.0, 'silver')
    """, (alice_id, mono_id))

    cursor_db.execute("""
        INSERT INTO Account (user_id, type, account_num, bank_id, currency, amount, status)
        VALUES (?, 'debit', 'UA1111222233', ?, 'USD', 1000.0, 'platinum')
    """, (bob_id, mono_id))

    cursor_db.execute("SELECT id FROM Account WHERE account_num = 'UA1234567890'")
    acc1_id = cursor_db.fetchone()[0]
    cursor_db.execute("SELECT id FROM Account WHERE account_num = 'UA1111222233'")
    acc2_id = cursor_db.fetchone()[0]

    cursor_db.execute("""
        INSERT INTO Transactions (
            bank_sender_name, account_sender_id,
            bank_receiver_name, account_receiver_id,
            sent_currency, sent_amount, datetime
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ('MonoBank', acc2_id, 'PrivatBank', acc1_id, 'USD', 200.0, '2025-06-01 12:00:00'))


@pytest.fixture
def temp_test_db():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    create_tables_for_db(cursor)
    insert_general_test_data(cursor)

    conn.commit()
    cursor.close()

    with patch('sqlite3.connect', return_value=conn):
        yield conn


@pytest.fixture
def mock_validate_fields_on_add_account():
    with patch('homework_4.adding_data_to_DB.validate_fields')as patched:
        yield patched


@pytest.fixture
def mock_validate_fields_on_update_account():
    with patch('homework_4.modify_data_in_DB.validate_fields') as patched:
        yield patched


@pytest.fixture
def mock_validate_account_number_on_add_account():
    with (patch('homework_4.adding_data_to_DB.validate_account_number', return_value='ID--a-b-q-123456-u')
          as patched):
        yield patched


@pytest.fixture
def mock_validate_account_number_on_update_account():
    with (patch('homework_4.modify_data_in_DB.validate_account_number', return_value='ID--jh-p-001273-xz')
          as patched):
        yield patched
