import logging
from setup_logging import init_logger
from consts import LOGGER_NAME
from adding_data_to_DB import add_users, add_banks, add_accounts, add_data_from_csv
from test_data import load_test_data_in_csv_users, load_test_data_in_csv_banks, load_test_data_in_csv_accounts
from modify_data_in_DB import modify_user, modify_bank, modify_account
from delete_data_in_DB import delete_user, delete_bank, delete_account
from transfer_operations import send_money
from database_services import (get_random_credit_discount, get_users_with_debts, get_bank_with_largest_capital,
                               get_bank_serving_oldest_client, get_bank_with_most_outbound_users,
                               delete_users_without_full_info, get_transactions_last_3_months)


def main():
    init_logger(LOGGER_NAME)
    logger = logging.getLogger(LOGGER_NAME)
    logger.info('Launching the application')

    load_test_data_in_csv_users('/Users/dmitrijmaruhna/Desktop/test_users.csv')
    load_test_data_in_csv_banks('/Users/dmitrijmaruhna/Desktop/test_banks.csv')
    load_test_data_in_csv_accounts('/Users/dmitrijmaruhna/Desktop/test_accounts.csv')

    add_data_from_csv('/Users/dmitrijmaruhna/Desktop/test_users.csv', add_users)
    add_data_from_csv('/Users/dmitrijmaruhna/Desktop/test_banks.csv', add_banks)
    add_data_from_csv('/Users/dmitrijmaruhna/Desktop/test_accounts.csv', add_accounts)

    modify_user(1, 'name', 'Client')
    modify_bank(1, 'name', 'PrivatBank')
    modify_account(1, 'type', 'credit')

    send_money(1, 3, 100)

    answer_1 = get_random_credit_discount()
    for user_id, user_discount in answer_1.items():
        print(f'User ID: {user_id}. Discount given to him: {user_discount}.')

    answer_2 = get_users_with_debts()
    print('Users with debts:')
    for item in answer_2:
        print(f'{item[0]} {item[1]}')

    send_money(4, 5, 3000)

    print(f'Bank with largest capital: {get_bank_with_largest_capital()[0]}')
    print(f'The oldest bank client: {get_bank_serving_oldest_client()[0]}')
    print(f'Bank with the highest number of outgoing transactions: {get_bank_with_most_outbound_users()[0]}')

    delete_users_without_full_info()

    print(f'Transactions for the last 3 months: {get_transactions_last_3_months(1)}')

    logger.info('Closing the application')


if __name__ == '__main__':
    main()
