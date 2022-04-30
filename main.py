from tkinter import *
from tkinter import messagebox
import sqlite3
import pandas as pd
import helpers.hash_password as bcrypt


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

    def closeDatabase(self):
        self.connection.close()


# db = DATABASE()
# print(db.query('SELECT * FROM accounts'))


class Login:
    def __init__(self, login=Tk()):
        self.login = login
        login.protocol("WM_DELETE_WINDOW", self.close)
        login.geometry("340x300")
        login.title("Login")
        # if user logs in return id
        # variable gives information about the user to the main window
        self.user_id = 0

        self.user_email = Entry(login, width=35)
        self.user_password = Entry(login, width=35)
        self.login_btn = Button(login, text="Login", width=35,
                                command=self.handle_login)
        self.register_btn = Button(login, text="open account", width=35,
                                   command=self.register_ui)

        # text fields
        # email_text = Text(root, )

        # add to window
        self.user_email.grid(row=1, column=3, columnspan=5, sticky=E+W)
        self.user_password.grid(row=2, column=3, columnspan=5, sticky=E+W)
        self.login_btn.grid(row=3, column=3, columnspan=5, sticky=E+W)
        self.register_btn.grid(row=4, column=3, columnspan=5)

    def close(self):
        exit()

    def handle_login(self):
        email = self.user_email.get()
        password = self.user_password.get()

        if not email or not password:
            msg = Label(
                self.login, text="Please include an email address and password")
            msg.grid(row=6, column=0)
            return
        try:
            db = DATABASE()
            user = db.findByEmail(email)
            user = user.to_dict()

            if bcrypt.validateHash(password, user['password'][0]):
                print('user logged in')
                self.user_id = user['id'][0]
                self.login.destroy()  # removes this window
                return
            else:
                messagebox.showwarning(
                    title='Invalid input', message='Email or password is incorrect')
                return
        except Exception as e:
            print(e)

        messagebox.showwarning(
            title='User', message='User does not exist')

        return

    def register_ui(self):
        win = Toplevel(self.login)
        self.win = win
        win.title("Register")

        # Input fields
        self.first_entry = Entry(win, width=32)
        self.last_entry = Entry(win, width=32)
        self.email_entry = Entry(win, width=32)
        self.password_entry = Entry(win, width=32)

        # labels
        self.first_label = Label(win, text="First name")
        self.last_label = Label(win, text="Last name")
        self.email_label = Label(win, text="email")
        self.password_label = Label(win, text="password")

        # button
        self.register_btn = Button(
            win, text="create", command=self.create_account)

        # place on register window
        self.first_label.grid(row=0, column=0, sticky='w')
        self.first_entry.grid(row=0, column=1, sticky=E+W)

        self.last_label.grid(row=1, column=0, sticky='w')
        self.last_entry.grid(row=1, column=1, sticky=E+W)

        self.email_label.grid(row=2, column=0, sticky='w')
        self.email_entry.grid(row=2, column=1, sticky=E+W)

        self.password_label.grid(row=3, column=0, sticky='w')
        self.password_entry.grid(row=3, column=1, sticky=E+W)

        self.register_btn.grid(row=4, column=0, columnspan=5, sticky=E+W)

    def create_account(self):
        first = self.first_entry.get()
        last = self.last_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        hashed = bcrypt.generateHash(password)
        print(len(hashed))
        db = DATABASE()
        res = db.add_account(first, last, email, hashed)

        if res:
            messagebox.showinfo(title="User created", message="user created")
            self.win.destroy()
        else:
            messagebox.showwarning(title="Error", message="server error")

    def mainloop_window(self):
        self.login.mainloop()


# login_page = Login()
# login_page.mainloop_window()


class BANK_MANAGEMENT:
    def __init__(self, root=Tk()):
        self.root = root
        root.title("Bank management")
        root.geometry('600x400')

        frame1 = Frame(root, width=520, height=200, highlightbackground='red',
                       highlightthickness=3)
        frame1.grid(row=0, column=0, padx=20, pady=10, ipadx=20)

        label = Label(frame1, text="window1", font=(16))
        label.grid(row=0, column=0)

    def mainloop_root(self, user_id):
        print(f'MAIN WINDOW {user_id}')
        self.root.mainloop()


main_win = BANK_MANAGEMENT()
main_win.mainloop_root(5)
# main_win.mainloop_root(login_page.user_id)
