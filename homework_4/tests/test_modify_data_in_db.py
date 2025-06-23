from homework_4.modify_data_in_db import modify_user, modify_bank, modify_account
from homework_4.consts import SQL_UPDATE_USER_FIELD, SQL_UPDATE_BANK_FIELD, SQL_UPDATE_ACCOUNT_FIELD
from unittest.mock import patch


def test_modify_user(mock_db_cursor):
    test_input = [1, 'name', 'Testing']

    result = modify_user(*test_input)

    expected_sql = SQL_UPDATE_USER_FIELD.format('name')
    mock_db_cursor.execute.assert_any_call(expected_sql, ('Testing', 1))

    assert result == 'Successfully changed field name in table User'


def test_modify_bank(mock_db_cursor):
    test_input = [1, 'name', 'NewPrivat24']

    result = modify_bank(*test_input)

    expected_sql = SQL_UPDATE_BANK_FIELD.format('name')
    mock_db_cursor.execute.assert_any_call(expected_sql, ('NewPrivat24', 1))

    assert result == 'Successfully changed field name in table Bank'


def test_modify_account(mock_validate_account_number_on_update_account, mock_validate_fields_on_update_account,
                        mock_db_cursor, valid_account_num, valid_account_type, valid_status):
    test_input_1 = [1, 'account_num', valid_account_num]
    test_input_2 = [1, 'type', valid_account_type]
    test_input_3 = [1, 'status', valid_status]

    result_1 = modify_account(*test_input_1)

    expected_sql = SQL_UPDATE_ACCOUNT_FIELD.format('account_num')
    mock_db_cursor.execute.assert_any_call(expected_sql, (valid_account_num, 1))

    result_2 = modify_account(*test_input_2)

    expected_sql = SQL_UPDATE_ACCOUNT_FIELD.format('type')
    mock_db_cursor.execute(expected_sql, valid_account_type, 1)

    result_3 = modify_account(*test_input_3)

    expected_sql = SQL_UPDATE_ACCOUNT_FIELD.format('status')
    mock_db_cursor.execute.assert_any_call(expected_sql, (valid_status, 1))

    assert result_1 == 'Successfully changed field account_num in table Account'
    assert result_2 == 'Successfully changed field type in table Account'
    assert result_3 == 'Successfully changed field status in table Account'
