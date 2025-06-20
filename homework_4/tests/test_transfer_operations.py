from unittest.mock import MagicMock, patch
from homework_4.transfer_operations import send_money, convert_currency
from homework_4.consts import SQL_UPDATE_ACCOUNT_AFTER_TRANSACTION, SQL_SELECT_ACCOUNT_INFO, SQL_INSERT_TRANSACTION


def test_send_money_success(mock_convert_currency, mock_db_cursor):
    mock_db_cursor.execute.side_effect = [
        None,
        MagicMock(fetchone=lambda: (300, 'USD', 1)),
        MagicMock(fetchone=lambda: (100, 'EUR', 2)),
        None,
        None,
        MagicMock(fetchone=lambda: ('Privat24',)),
        MagicMock(fetchone=lambda: ('Mono',)),
        None
    ]

    result = send_money(1, 2, 80, transaction_date='2025-06-18 15:10')

    mock_db_cursor.execute.assert_any_call(SQL_SELECT_ACCOUNT_INFO, (1,))
    mock_db_cursor.execute.assert_any_call(SQL_SELECT_ACCOUNT_INFO, (2,))
    mock_db_cursor.execute.assert_any_call(SQL_UPDATE_ACCOUNT_AFTER_TRANSACTION, (220, 1))
    mock_db_cursor.execute.assert_any_call(SQL_UPDATE_ACCOUNT_AFTER_TRANSACTION, (200, 2))
    mock_db_cursor.execute.assert_any_call(SQL_INSERT_TRANSACTION, ('Privat24', 1, 'Mono', 2, 'USD', 80,
                                                                    '2025-06-18 15:10'))
    mock_convert_currency.assert_called_once_with('USD', 'EUR', 80)

    assert result == 'Transaction from ID 1 to ID 2 completed successfully.'


def test_convert_currency(mock_request_get, mock_os_getenv, mock_load_dotenv, api_response):
    input_data = ['USD', 'EUR', 100]

    mock_request_get.json.return_value = api_response
    result = convert_currency(*input_data)

    assert result == 90.0

