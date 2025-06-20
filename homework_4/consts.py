LOGGER_NAME = 'LAB_4_LOGGER'

ALLOWED_STATUSES = ['gold', 'silver', 'platinum']
ALLOWED_TYPES = ['credit', 'debit']

SIZE_ACC_NUM = 18

DISCOUNTS = [25, 30, 50]

SQL_INSERT_USER = '''INSERT INTO User(name, surname, birth_day)
                     VALUES(?, ?, ?)'''
SQL_INSERT_BANK = '''INSERT INTO Bank(name)
                     VALUES(?)'''
SQL_INSERT_ACCOUNT = '''INSERT INTO Account(user_id, type, account_num, bank_id, currency, amount, status)
                        VALUES(?, ?, ?, ?, ?, ?, ?)'''
SQL_INSERT_TRANSACTION = '''INSERT INTO Transactions(
                              bank_sender_name,
                              account_sender_id,
                              bank_receiver_name,
                              account_receiver_id,
                              sent_currency,
                              sent_amount,
                              datetime)
                          VALUES (?, ?, ?, ?, ?, ?, ?)'''

SQL_SELECT_ACCOUNT_INFO = '''SELECT amount, currency, bank_id
                             FROM Account
                             WHERE id = ?'''
SQL_SELECT_BANK_NAME = '''SELECT name
                          FROM Bank
                          WHERE id = ?'''
SQL_SELECT_RANDOM_ID_USER_WITH_LIMIT = '''SELECT ID
                                          FROM User
                                          ORDER BY RANDOM() LIMIT {}'''
SQL_SELECT_USERS_WITH_DEBTS = '''SELECT name, surname
                                 FROM User
                                 INNER JOIN Account ON Account.user_id = User.id
                                 WHERE Account.amount < 0;'''
SQL_SELECT_BANK_WITH_LARGEST_CAPITAL = '''SELECT name
                                          FROM Bank
                                          INNER JOIN Account ON Account.bank_id = Bank.id
                                          GROUP BY Bank.id
                                          ORDER BY SUM(Account.amount) DESC
                                          LIMIT 1'''
SQL_SELECT_BANK_SERVING_OLDEST_CLIENT = '''SELECT Bank.name
                                           FROM Bank
                                           INNER JOIN Account ON Account.bank_id = Bank.id
                                           INNER JOIN User ON Account.user_id = User.id
                                           GROUP BY Bank.id
                                           ORDER BY MIN(User.birth_day) ASC
                                           LIMIT 1'''
SQL_SELECT_BANK_WITH_MOST_OUTBOUND_USERS = '''SELECT Bank.name
                                              FROM Bank
                                              INNER JOIN Account ON Account.bank_id = Bank.id
                                              INNER JOIN Transactions ON Transactions.account_sender_id = Account.id
                                              INNER JOIN User ON User.id = Account.user_id
                                              GROUP BY Bank.id
                                              ORDER BY COUNT(DISTINCT User.id) DESC
                                              LIMIT 1'''
SQL_SELECT_TRANSACTIONS_LAST_3_MONTHS = '''SELECT *
                                               FROM Transactions
                                               WHERE (
                                                   account_sender_id IN (SELECT id FROM Account
                                                   WHERE user_id = {})
                                                   OR account_receiver_id IN (SELECT id FROM Account
                                                   WHERE user_id = {})
                                              )
                                              AND datetime >= DATE('now', '-3 months');'''

SQL_UPDATE_USER_FIELD = 'UPDATE User SET {} = ? WHERE id = ?'
SQL_UPDATE_BANK_FIELD = 'UPDATE Bank SET {} = ? WHERE id = ?'
SQL_UPDATE_ACCOUNT_FIELD = 'UPDATE Account SET {} = ? WHERE id = ?'
SQL_UPDATE_ACCOUNT_AFTER_TRANSACTION = '''UPDATE Account
                                          SET amount = ?
                                          WHERE id = ?'''

SQL_DELETE_USER = 'DELETE FROM User WHERE id = ?'
SQL_DELETE_BANK = 'DELETE FROM Bank WHERE id = ?'
SQL_DELETE_ACCOUNT = 'DELETE FROM Account WHERE id = ?'
SQL_DELETE_USERS_WITHOUT_FULL_INFO = '''DELETE FROM User
                                        WHERE name = '' OR surname = '' OR birth_day = '';'''

SQL_CREATE_TABLE_BANK_FOR_TEST = '''CREATE TABLE IF NOT EXISTS Bank (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name TEXT NOT NULL UNIQUE
                                    )'''
SQL_CREATE_TABLE_USER_FOR_TEST = f'''CREATE TABLE IF NOT EXISTS User (
                                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                                     name TEXT NOT NULL,
                                     surname TEXT NOT NULL,
                                     birth_day TEXT,
                                     accounts TEXT
                                     )'''
SQL_CREATE_TABLE_ACCOUNT_FOR_TEST = '''CREATE TABLE IF NOT EXISTS Account (
                                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                                       user_id INT NOT NULL,
                                       type TEXT NOT NULL CHECK(type IN ('credit', 'debit')),
                                       account_num TEXT NOT NULL UNIQUE,
                                       bank_id INT NOT NULL,
                                       currency TEXT NOT NULL,
                                       amount REAL NOT NULL,
                                       status TEXT NOT NULL CHECK(status IN ('gold', 'silver', 'platinum')),
                                       FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
                                       FOREIGN KEY (bank_id) REFERENCES Bank(id) ON DELETE CASCADE
                                       )'''
SQL_CREATE_TABLE_TRANSACTIONS_FOR_TEST = '''CREATE TABLE IF NOT EXISTS Transactions (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            bank_sender_name TEXT NOT NULL,
                                            account_sender_id INT NOT NULL,
                                            bank_receiver_name TEXT NOT NULL,
                                            account_receiver_id INT NOT NULL,
                                            sent_currency TEXT NOT NULL,
                                            sent_amount REAL NOT NULL,
                                            datetime TEXT,
                                            FOREIGN KEY (account_sender_id) REFERENCES Account(id) ON DELETE CASCADE,
                                            FOREIGN KEY (account_receiver_id) REFERENCES Account(id) ON DELETE CASCADE
                                            )'''