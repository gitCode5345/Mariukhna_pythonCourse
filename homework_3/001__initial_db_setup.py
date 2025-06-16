import sqlite3
import argparse


def init_tables_db(args_param):
    conn = sqlite3.connect('./homework_3/bank_data.db')
    cursor = conn.cursor()

    cursor.execute('PRAGMA foreign_keys = ON;')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Bank (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE
                        )''')
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS User (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        surname TEXT NOT NULL,
                        birth_day TEXT,
                        accounts TEXT
                        {', UNIQUE(name, surname)' if args_param == 1 else ''}
                        )''')
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS Account (
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
                        )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Transactions (
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
                        )''')

    conn.commit()
    cursor.close()
    conn.close()


parser = argparse.ArgumentParser()
parser.add_argument('--unique', type=int, help='If you want the user.name and user.surname fields\
                    to be unique, specify 1, otherwise 0')
args = parser.parse_args()

if args.unique not in [0, 1]:
    parser.error("--unique must be 0 or 1")

init_tables_db(args.unique)
