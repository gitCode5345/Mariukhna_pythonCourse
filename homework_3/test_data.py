import csv


def load_test_data_in_csv_users(path: str):
    fieldnames = ['user_fullname', 'birth_day']
    data = [{'user_fullname': 'John Test', 'birth_day': '2010-10-11'},
            {'user_fullname': 'John Tested', 'birth_day': '2010-11-5'},
            {'user_fullname': 'Client Oldest', 'birth_day': '1995-11-10'},
            {'user_fullname': 'New Test', 'birth_day': None}]
    with open(path, mode='w') as file:
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(data)


def load_test_data_in_csv_banks(path: str):
    fieldnames = ['bank_name']
    data = [{'bank_name': 'Privat'},
            {'bank_name': 'Mono'}]
    with open(path, mode='w') as file:
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(data)


def load_test_data_in_csv_accounts(path: str):
    fieldnames = ['user_id', 'account_num', 'bank_id', 'currency', 'amount', 'status', 'type']
    data = [
        {
            'user_id': '1',
            'account_num': 'ID--a#b-q-123456-u',
            'bank_id': '1',
            'currency': 'USD',
            'amount': 1500.50,
            'status': 'gold',
            'type': 'debit'
        },
        {
            'user_id': '2',
            'account_num': 'ID--tz-q-120394-uf',
            'bank_id': '1',
            'currency': 'USD',
            'amount': -100.00,
            'status': 'silver',
            'type': 'credit'
        },
        {
            'user_id': '1',
            'account_num': 'ID--mv-w-457829-ld',
            'bank_id': '2',
            'currency': 'EUR',
            'amount': 250.75,
            'status': 'platinum',
            'type': 'debit'
        },
        {
            'user_id': '3',
            'account_num': 'ID--jh-p-001273-xz',
            'bank_id': '1',
            'currency': 'USD',
            'amount': 3000.00,
            'status': 'gold',
            'type': 'credit'
        },
        {
            'user_id': '2',
            'account_num': 'ID--qe-y-783026-mr',
            'bank_id': '2',
            'currency': 'USD',
            'amount': 75.20,
            'status': 'silver',
            'type': 'debit'
        }
    ]
    with open(path, mode='w') as file:
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(data)
