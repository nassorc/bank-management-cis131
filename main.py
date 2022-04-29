from tkinter import *
import sqlite3


class DATABASE:
    def __init__(self):
        self.FIRSTNAME = ""
        self.LASTNAME = ""
        self.EMAIL = ""


class Login:
    def __init__(self, login=Tk()):
        self.login = login
        login.protocol("WM_DELETE_WINDOW", self.close)
        login.geometry("340x300")
        login.title("Login")

        self.user_email = Entry(login, width=35)
        self.user_password = Entry(login, width=35)
        self.login_btn = Button(login, text="Login", width=35,
                                command=self.handle_login)
        self.register_btn = Button(login, text="open account", width=35,
                                   command=self.handle_register)

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
        user = ['mat', '123']
        email = self.user_email.get()
        password = self.user_password.get()

        if not email or not password:
            msg = Label(
                self.login, text="Please include an email address and password")
            msg.grid(row=5, column=2)
            return
        try:
            if email == user[0] and password == user[1]:
                print('user logged in')
                self.login.destroy()  # removes this window
        except Exception as e:
            print(e)

        return

    def handle_register():
        return

    def mainloop_window(self):
        self.login.mainloop()


login_page = Login()
login_page.mainloop_window()


class BANK_MANAGEMENT:
    def __init__(self, root=Tk()):
        self.root = root
        root.title("Bank management")

    def mainloop_root(self):
        self.root.mainloop()


main_win = BANK_MANAGEMENT()
main_win.mainloop_root()
