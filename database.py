import sqlite3
import pandas as pd


class DATABASE:
    def __init__(self):
        self.FIRSTNAME = ""
        self.LASTNAME = ""
        self.EMAIL = ""
        try:
            self.connection = sqlite3.connect('accounts.db')
        except Exception as e:
            print("Error: Database class could not establish connection with database.")

    def query(self, query):
        return pd.read_sql(query, self.connection)

    def add_account(self, first, last, email, password):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                f"INSERT INTO accounts (email, password, first_name, last_name) VALUES('{email}', '{password.decode('ASCII')}', '{first}', '{last}');")
        except Exception as e:
            print(f"Error: addAccount did not create new user\n--{e}")
            return False

        self.connection.commit()
        return True

    def findByEmail(self, email):
        return pd.read_sql(f"SELECT * FROM accounts WHERE email='{email}'", self.connection)

    def findById(self, id):
        return pd.read_sql(f"SELECT * FROM accounts WHERE id={id}", self.connection)

    def closeDatabase(self):
        self.connection.close()


# db = DATABASE()
# print(db.query('SELECT * FROM accounts'))
