import re
from datetime import datetime


def validate_user_full_name(full_name):
    """
    Splits the full name into first name and surname, removing non-alphabetic characters.
    """
    parts = re.findall(r"[A-Za-z']+", full_name)
    if len(parts) < 2:
        raise ValueError("Full name must contain at least a first name and a surname.")

    name = parts[0]
    surname = " ".join(parts[1:])
    return name, surname


def validate_enum(field_name, value, allowed_values):
    """
    Checks if the value is in the list of allowed values.
    """
    if value not in allowed_values:
        raise ValueError(f"Not allowed value '{value}' for field '{field_name}'!")
    return value


def validate_account_number(account_number):
    """
    Cleans and checks the account number format.
    Requirements:
    - Replaces #%_?& characters with a hyphen (-).
    - The string length must be exactly 18 characters.
    - Must start with "ID--".
    - Must contain a pattern: 1-3 letters, hyphen, one or more digits, hyphen (anywhere after the prefix).
    Example of valid format (though the specific structure may vary after ID--): ID--abc-1234567-x9
    Example with requirements: ID--j3-q-432547-u9
    """
    cleaned_account_number = re.sub(r"[#%_?&]", "-", account_number)

    if len(cleaned_account_number) < 18:
        raise ValueError("Account number too few characters!")
    if len(cleaned_account_number) > 18:
        raise ValueError("Account number too many characters!")

    if not cleaned_account_number.startswith("ID--"):
        raise ValueError("Account number wrong format!")
    if not re.search(r"[A-Za-z]{1,3}-\d+-", cleaned_account_number):
        raise ValueError("Account number broken ID!")

    return cleaned_account_number


def get_current_datetime():
    """
    Returns the current date and time as a string.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
