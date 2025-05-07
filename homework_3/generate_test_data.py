import csv


def create_test_csv_user(path):
    fieldnames = ['user_full_name', 'birth_day', 'accounts']
    rows = [
        {'user_full_name': 'John Doe', 'birth_day': '1990-01-01'},
        {'user_full_name': 'Anna Smith', 'birth_day': '1985-08-22'},
    ]

    with open(path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def create_test_csv_bank(path):
    fieldnames = ['name']
    rows = [
        {'name': 'PrivatBank'},
        {'name': 'MonoBank'}
    ]

    with open(path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def create_test_csv_account(path):
    fieldnames = ['user_id', 'type', 'account_num', 'bank_id', 'currency', 'amount', 'status']
    rows = [
        {
            'user_id': 1,
            'type': 'debit',
            'account_num': 'ID--abc-1234567-x9',
            'bank_id': 1,
            'currency': 'USD',
            'amount': 1500.00,
            'status': 'active'
        },
        {
            'user_id': 1,
            'type': 'credit',
            'account_num': 'ID--j3-q-432547-u9',
            'bank_id': 2,
            'currency': 'EUR',
            'amount': 300.00,
            'status': 'active'
        },
        {
            'user_id': 2,
            'type': 'debit',
            'account_num': 'ID--xy-12345678-ab',
            'bank_id': 1,
            'currency': 'USD',
            'amount': 800.00,
            'status': 'active'
        },
        {
            'user_id': 2,
            'type': 'debit',
            'account_num': 'ID--z-123456789-0c',
            'bank_id': 2,
            'currency': 'USD',
            'amount': 1000.00,
            'status': 'active'
        },
        {
            'user_id': 3,
            'type': 'credit',
            'account_num': 'ID--ghk-1234567-ef',
            'bank_id': 1,
            'currency': 'GBP',
            'amount': 2000.00,
            'status': 'active'
        },
    ]

    with open(path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
