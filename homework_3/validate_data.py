import re
from consts import SIZE_ACC_NUM


def validate_user_name(full_name: str):
    """
    description:
    validate and split full name into first name and surname

    :param full_name: string containing user's full name (e.g. 'John Smith')

    :return: --> tuple (name, surname) or raises ValueError if invalid
    """
    parts = re.findall(r'[A-Za-z\']+', full_name)
    if len(parts) < 2:
        raise ValueError("Full name must contain at least a first name and a surname.")

    name = parts[0]
    surname = " ".join(parts[1:])
    return name, surname


def validate_fields(field_name, variable_value, allowed_values):
    """
    description:
    check if the value of a field is in the list of allowed values

    :param field_name: name of the field being validated
    :param variable_value: value to validate
    :param allowed_values: list of permitted values for the field

    :return: --> void or raises ValueError if value is not allowed
    """
    if variable_value not in allowed_values:
        raise ValueError(f'Not allowed value {variable_value} for field {field_name}')


def validate_account_number(acc_num: str):
    """
    description:
    validate and sanitize an account number by checking length, format, and pattern,
    and replacing special characters with dashes

    :param acc_num: raw account number string to validate

    :return: --> str (cleaned account number) or raises ValueError if invalid
    """
    if not len(acc_num) == SIZE_ACC_NUM:
        raise ValueError(f'Incorrect account number length should be {SIZE_ACC_NUM}')
    elif not acc_num.startswith('ID--'):
        raise ValueError(f'Invalid format. Account number must start with ID--')

    clean_acc_num = re.sub(r'[#%_?&]', '-', acc_num)
    search_pattern = r'[a-zA-Z]{1,3}-\d+-'
    if not re.search(search_pattern, clean_acc_num):
        raise ValueError('Broken ID')

    return clean_acc_num
