from tkinter import *
from tkinter import messagebox
import sqlite3
import pandas as pd
import helpers.hash_password as bcrypt
import database


class Login:
    def __init__(self, login_window=Tk()):
        self.login_window = login_window
        # this prevent opening the main window when clicking close without
        # logging in
        login_window.protocol("WM_DELETE_WINDOW", self.close)
        login_window.geometry("410x300")
        login_window.title("Login")
        # if user logs in return id
        # variable gives information about the user to the main window
        self.user_id = 0

        self.login_frame = Frame(
            login_window, width=340, height=300, padx=20)

        self.login_logo = Label(
            self.login_frame, text="Bank Manager", font=48, pady=15)
        self.login_email_label = Label(self.login_frame, text="email")
        self.login_password_label = Label(self.login_frame, text="password")
        self.user_email = Entry(self.login_frame, width=35)
        self.user_password = Entry(self.login_frame, width=35, show="*")
        self.login_btn = Button(self.login_frame, text="Login", width=35,
                                command=self.handle_login)
        self.register_btn = Button(self.login_frame, text="open account", width=35,
                                   command=self.register_ui)

        # text fields
        # email_text = Text(root, )

        # add to window
        self.login_logo.grid(row=0, column=2)
        self.login_email_label.grid(row=1, column=2, sticky=W)
        self.login_password_label.grid(row=2, column=2, sticky=W)
        self.user_email.grid(row=1, column=3, columnspan=5, sticky=E+W)
        self.user_password.grid(row=2, column=3, columnspan=5, sticky=E+W)
        self.login_btn.grid(row=3, column=3, columnspan=5, sticky=E+W)
        self.register_btn.grid(row=4, column=3, columnspan=5)

        self.login_frame.pack()

    def close(self):
        exit()

    def handle_login(self):
        email = self.user_email.get()
        password = self.user_password.get()

        if not email or not password:
            # msg = Label(
            #     self.login_window, text="Please include an email address and password")
            # msg.place()
            messagebox.showwarning(
                title="incomplete", message='Please include an email and password')
            return
        try:
            db = database.DATABASE()
            user = db.findByEmail(email)
            user = user.to_dict()

            if bcrypt.validateHash(password, user['password'][0]):
                print('user logged in')
                self.user_id = user['id'][0]
                self.login_window.destroy()  # removes this window
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
        register_window = Toplevel(self.login_window)
        self.register_window = register_window
        register_window.title("Register")

        # Input fields
        self.first_entry = Entry(register_window, width=32)
        self.last_entry = Entry(register_window, width=32)
        self.email_entry = Entry(register_window, width=32)
        self.password_entry = Entry(register_window, width=32)

        # labels
        self.first_label = Label(register_window, text="First name")
        self.last_label = Label(register_window, text="Last name")
        self.email_label = Label(register_window, text="email")
        self.password_label = Label(register_window, text="password")

        # button
        self.register_btn = Button(
            register_window, text="create", command=self.create_account)

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
        db = database.DATABASE()
        res = db.add_account(first, last, email, hashed)

        if res:
            messagebox.showinfo(title="User created", message="user created")
            self.register_window.destroy()
        else:
            messagebox.showwarning(title="Error", message="server error")

    def mainloop_window(self):
        self.login_window.mainloop()


login_page = Login()
db = database.DATABASE()

login_page.mainloop_window()


class BANK_MANAGEMENT:
    def __init__(self, user_id, root=Tk()):
        self.root = root
        root.title("Bank management")
        root.geometry('600x400')

        # get user information
        self.user_id = user_id
        db = database.DATABASE()
        self.user = db.findById(self.user_id).to_dict()

        self.frame1 = LabelFrame(root, width=520, height=100, padx=10, pady=10)
        self.frame1.grid(row=0, column=0, columnspan=2,
                         padx=20, pady=10, ipadx=20, sticky=E+W)

        self.logo_label = Label(self.frame1, text="Bank Management", font=(48))
        self.logo_label.place(relx=.04, rely=.35)

        self.user_email_label = Label(
            self.frame1, text=f"email: {self.user['email'][0]}")
        self.user_email_label.place(relx=.70, rely=.15)

        self.balance_label = Label(
            self.frame1, text=f"Balance: ${self.user['balance'][0]}")
        self.balance_label.place(relx=.70, rely=.45)

        self.frame2 = Frame(root, width=520, height=60)
        self.frame2.grid(row=1, columnspan=2,
                         padx=20, pady=10, sticky=E+W)

        self.deposit_btn = Button(self.frame2, text="deposit", width=18)
        self.deposit_btn.grid(row=0, column=0, padx=3)

        self.withdraw_btn = Button(self.frame2, text="withdraw", width=18)
        self.withdraw_btn.grid(row=0, column=1)

        self.transfer_btn = Button(self.frame2, text="transfer", width=18)
        self.transfer_btn.grid(row=0, column=2)

        self.activity_btn = Button(self.frame2, text="activity", width=18)
        self.activity_btn.grid(row=0, column=3)

    def mainloop_root(self):
        self.root.mainloop()


# main_win = BANK_MANAGEMENT(5)
main_win = BANK_MANAGEMENT(login_page.user_id)
main_win.mainloop_root()
