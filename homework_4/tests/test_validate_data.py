from homework_4.validate_data import validate_user_name, validate_fields, validate_account_number


def test_validate_user_name(valid_user_name):
    expected_value = ('John', 'Test')
    result = validate_user_name(valid_user_name)
    assert expected_value == result


def test_validate_fields(valid_account_type, valid_account_types):
    expected_value = None
    result = validate_fields('acc_type', valid_account_type, valid_account_types)
    assert expected_value == result


def test_validate_account_number(valid_account_num_with_replace):
    expected_value = 'ID--jh-p-0-12-3-xz'
    result = validate_account_number(valid_account_num_with_replace)
    assert expected_value == result

