import sqlite3
import pandas as pd


class DATABASE:
    """
    Database class stores database related functions.
    """

    def __init__(self):
        # connect to database
        try:
            self.connection = sqlite3.connect('accounts.db')
        except Exception as e:
            print("Error: Database class could not establish connection with database.")

    def query(self, query):
        # function queries database given a query argument
        return pd.read_sql(query, self.connection)

    def add_transaction_record(self, id, amount):
        # function adds a transaction
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                f"INSERT INTO transactions (account_id, amount) VALUES('{id}', {amount});")
        except Exception as e:
            print(
                f"Error: add_transaction_record failed to insert new recrod.\n--{e}")
            return False

        # commit changes to database
        self.connection.commit()
        return True

    def add_transfer_record(self, receiver, sender, amount):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                f"INSERT INTO transfers (from_account, to_account, amount) VALUES({receiver},{sender},{amount});")
        except Exception as e:
            print(
                f"Error: add_transfer_record failed to insert new record.\n--{e}")
            return False

        self.connection.commit()
        return True

    def add_account(self, first, last, email, password):
        # function creates and inserts a new user into the database
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                f"INSERT INTO accounts (email, password, first_name, last_name) VALUES('{email}', '{password.decode('ASCII')}', '{first}', '{last}');")
        except Exception as e:
            print(f"Error: addAccount did not create new user\n--{e}")
            return False

        # commit changes to database
        self.connection.commit()
        return True

    def findByEmail(self, email):
        # finds a user given an email
        return pd.read_sql(f"SELECT * FROM accounts WHERE email='{email}';", self.connection)

    def findById(self, id):
        # finds a user given an id
        return pd.read_sql(f"SELECT * FROM accounts WHERE id={id}", self.connection)

    def deposit_to_Account(self, id, amount):
        # function deposits an amount into a given users record
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"""UPDATE accounts SET balance = balance + {amount}
                                WHERE id = {id};""")
        except Exception as e:
            print(f"Error: depositToAccount failed.\n--{e}")
            return False

        self.connection.commit()
        self.add_transaction_record(id, amount)
        return True

    def withdraw_from_Account(self, id, amount):
        # function deposits an amount into a given users record
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"""UPDATE accounts SET balance = balance + {amount}
                                WHERE id = {id};""")
        except Exception as e:
            print(f"Error: depositToAccount failed.\n--{e}")
            return False

        self.connection.commit()
        self.add_transaction_record(id, amount)
        return True

    def closeDatabase(self):
        # this function closes the database
        self.connection.close()


# db = DATABASE()
# print(db.query("""
# SELECT *, tf.dt FROM accounts as a
# INNER JOIN transactions as t ON a.id = t.account_id
# INNER JOIN transfers as tf ON a.id = tf.from_account
# WHERE NOT EXISTS (SELECT * FROM transfers WHERE dt = tf.dt)
# """))
# print(db.query('SELECT * FROM transfers where from_account = 1002'))
# print(db.query('SELECT * FROM transfers'))
# db.add_account('matty', 'cross', 'matty@gmail.com', '321'.encode('ASCII'))
# print(db.query("""SELECT * FROM transfers"""))
