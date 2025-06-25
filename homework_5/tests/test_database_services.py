from homework_5.database_services import (get_random_credit_discount, get_users_with_debts,
                                          get_bank_with_most_outbound_users, get_bank_with_largest_capital,
                                          get_transactions_last_3_months, get_bank_serving_oldest_client,
                                          delete_users_without_full_info)
from unittest.mock import MagicMock
from homework_5.consts import SQL_DELETE_USERS_WITHOUT_FULL_INFO


def test_get_random_credit_discount(mock_rand_choice, mock_rand_int, mock_db_cursor, all_users_ids):
    mock_db_cursor.execute.side_effect = [None, MagicMock(fetchall=lambda: all_users_ids)]
    result = get_random_credit_discount()

    expected_value = {5: 25, 1: 30, 4: 50, 3: 25, 7: 30}
    assert expected_value == result


def test_get_users_with_debts(temp_test_db):
    result = get_users_with_debts()

    expected_value = [('Alice', 'Smith')]
    assert expected_value == result


def test_get_bank_with_largest_capital(temp_test_db):
    result = get_bank_with_largest_capital()

    expected_value = ('MonoBank',)
    assert expected_value == result


def test_get_bank_serving_oldest_client(temp_test_db):
    result = get_bank_serving_oldest_client()

    expected_value = ('MonoBank',)
    assert expected_value == result


def test_get_bank_with_most_outbound_users(temp_test_db):
    result = get_bank_with_most_outbound_users()

    expected_value = ('MonoBank',)
    assert expected_value == result


def test_delete_users_without_full_info(mock_db_cursor):
    result = delete_users_without_full_info()

    expected_value = 'Successfully removed users with incomplete information'
    mock_db_cursor.execute.assert_any_call(SQL_DELETE_USERS_WITHOUT_FULL_INFO)

    assert expected_value == result


def test_get_transactions_last_3_months(temp_test_db):
    input_user_id = 1
    result = get_transactions_last_3_months(input_user_id)

    expected_value = [(1, 'MonoBank', 3, 'PrivatBank', 1, 'USD', 200.0, '2025-06-01 12:00:00')]
    assert expected_value == result
