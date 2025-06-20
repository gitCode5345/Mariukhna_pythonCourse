from homework_4.delete_data_in_DB import delete_user, delete_bank, delete_account
from homework_4.consts import SQL_DELETE_USER, SQL_DELETE_BANK, SQL_DELETE_ACCOUNT


def test_delete_user(mock_db_cursor):
    test_id_user = 1

    result = delete_user(test_id_user)
    mock_db_cursor.execute.assert_any_call(SQL_DELETE_USER, (test_id_user,))

    assert result == 'Successfully deleted user with id 1'


def test_delete_bank(mock_db_cursor):
    test_id_bank = 1

    result = delete_bank(test_id_bank)
    mock_db_cursor.execute.assert_any_call(SQL_DELETE_BANK, (test_id_bank,))

    assert result == 'Successfully deleted bank with id 1'


def test_delete_account(mock_db_cursor):
    test_id_account = 1

    result = delete_account(test_id_account)
    mock_db_cursor.execute.assert_any_call(SQL_DELETE_ACCOUNT, (test_id_account,))

    assert result == 'Successfully deleted account with id 1'
