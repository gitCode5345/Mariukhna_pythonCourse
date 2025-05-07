import os
import logging
from generate_test_data import (
    create_test_csv_user,
    create_test_csv_bank,
    create_test_csv_account,
)
from api_module import (
    add_users_from_csv,
    add_banks_from_csv,
    add_accounts_from_csv,
    modify_user,
    modify_bank,
    modify_account,
    delete_user,
    delete_bank,
    delete_account,
    transfer_money
)
from get_information import (
    generate_random_discounts,
    get_users_with_debts,
    get_bank_with_largest_capital,
    get_bank_with_oldest_client,
    get_highest_number_of_unique_user_bank,
    delete_incomplete_users_and_accounts,
    get_user_transactions_last_3_months
)


def main():
    logging.basicConfig(level=logging.DEBUG)

    # user_csv_path = 'test_users.csv'
    # bank_csv_path = 'test_banks.csv'
    # account_csv_path = 'test_accounts.csv'
    #
    # create_test_csv_user(user_csv_path)
    # create_test_csv_bank(bank_csv_path)
    # create_test_csv_account(account_csv_path)
    #
    # print("Adding users from CSV:")
    # result = add_users_from_csv(user_csv_path)
    # print(result)
    #
    # print("Adding banks from CSV:")
    # result = add_banks_from_csv(bank_csv_path)
    # print(result)
    #
    # print("Adding accounts from CSV:")
    # result = add_accounts_from_csv(account_csv_path)
    # print(result)

    print("=== Random discounts ===")
    discounts = generate_random_discounts()
    for user_id, discount in discounts.items():
        print(f"User ID: {user_id} -> Discount: {discount}%")

    print("\n=== Users with debts ===")
    debtors = get_users_with_debts()
    for debtor in debtors:
        print(debtor)

    print("\n=== Bank with largest capital ===")
    largest_capital_bank = get_bank_with_largest_capital()
    print(f"Bank ID with largest capital: {largest_capital_bank}")

    print("\n=== Bank with oldest client ===")
    oldest_client_bank = get_bank_with_oldest_client()
    print(f"Bank name and customer's date of birth: {oldest_client_bank}")

    print("\n=== Bank with most unique users (by transactions) ===")
    top_bank = get_highest_number_of_unique_user_bank()
    print(f"Bank name with most unique users: {top_bank}")

    print("\n=== Deleting incomplete users and accounts ===")
    delete_incomplete_users_and_accounts()
    print("Incomplete users and accounts deleted (if any).")

    print("\n=== Transactions for user ID 1 in last 3 months ===")
    transactions = get_user_transactions_last_3_months(1)
    for tx in transactions:
        print(tx)

    print("Executing money transfer:")
    transfer_result = transfer_money(sender_account_id=2, receiver_account_id=9, amount=100)
    print(transfer_result)

    print("Test modifying user:")
    print(modify_user(user_id=2, new_name="Emily", new_surname="Girl"))

    print("\nTest modifying bank:")
    print(modify_bank(bank_id=4, new_name="Mono Updated"))

    print("\nTest modifying account:")
    print(modify_account(
        account_id=1,
        new_type="debit",
        new_currency="EUR",
        new_amount=2500.00,
        new_status="platinum"
    ))

    print("\nTest deleting account:")
    print(delete_account(account_id=3))

    print("\nTest deleting bank:")
    print(delete_bank(bank_id=2))

    print("\nTest deleting user:")
    print(delete_user(user_id=4))

    # os.remove(user_csv_path)
    # os.remove(bank_csv_path)
    # os.remove(account_csv_path)


if __name__ == "__main__":
    main()
