from homework_4.adding_data_to_db import add_users, add_banks, add_accounts, add_data_from_csv
from homework_4.consts import SQL_INSERT_USER, SQL_INSERT_BANK, SQL_INSERT_ACCOUNT
from unittest.mock import MagicMock


def test_add_users(mock_db_cursor):
    input_data = [
        {'user_fullname': 'John Doe', 'birth_day': '2000-01-01'},
        [
            {'user_fullname': 'Jane Smith', 'birth_day': '1999-12-31'},
            {'user_fullname': 'Alex Brown', 'birth_day': '2001-06-15'}
        ]
    ]

    result = add_users(*input_data)

    mock_db_cursor.execute.assert_any_call(SQL_INSERT_USER, ('John', 'Doe', '2000-01-01'))
    mock_db_cursor.execute.assert_any_call(SQL_INSERT_USER, ('Jane', 'Smith', '1999-12-31'))
    mock_db_cursor.execute.assert_any_call(SQL_INSERT_USER, ('Alex', 'Brown', '2001-06-15'))

    assert result == 'Successfully added user(s)'


def test_add_banks(mock_db_cursor):
    input_data = [{'bank_name': 'Privat'},
                  {'bank_name': 'Mono'}]

    result = add_banks(*input_data)

    mock_db_cursor.execute.assert_any_call(SQL_INSERT_BANK, ('Privat',))
    mock_db_cursor.execute.assert_any_call(SQL_INSERT_BANK, ('Mono',))

    assert result == 'Bank(s) successfully added to database'


def test_add_accounts(mock_validate_account_number_on_add_account, mock_validate_fields_on_add_account,
                      mock_db_cursor):
    input_data = [
        {
            'user_id': '1',
            'account_num': 'ID--a#b-q-123456-u',
            'bank_id': '1',
            'currency': 'USD',
            'amount': 1500.50,
            'status': 'gold',
            'type': 'debit'
        },
    ]

    result = add_accounts(*input_data)

    mock_db_cursor.execute.assert_any_call(
        SQL_INSERT_ACCOUNT,
        (1, 'debit', 'ID--a-b-q-123456-u', 1, 'USD', 1500.5, 'gold')
    )

    assert result == 'Successfully added account(s)'


def test_add_data_from_csv(sample_csv_file):
    mock_handler = MagicMock()
    result = add_data_from_csv(sample_csv_file, mock_handler)

    assert result == 'Data from CSV file successfully added'
    assert mock_handler.call_count == 2
    mock_handler.assert_any_call({'name': 'John', 'surname': 'Doe'})
    mock_handler.assert_any_call({'name': 'Jane', 'surname': 'Doe'})
