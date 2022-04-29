from tkinter import *


class BANK_MANAGEMENT_LOGIN:

    def __init__(self):
        self.EMAIL = ""
        self.PASSWORD = ""
        self.sys_message = ""

        def handle_login(email, password):
            user = ['mat', '123']
            if not email or not password:
                msg = Label(
                    root, text="Please include an email address and password")
                msg.grid(row=5, column=2)
                return (id)
            try:
                if email == user[0] and password == user[1]:
                    print('login')
            except Exception as e:
                print(e)

            return

        def handle_register():
            return

        root = Tk()

        root.geometry("340x300")
        root.title("Login")

        user_email = Entry(root, width=35)
        user_password = Entry(root, width=35)
        login_btn = Button(root, text="Login", width=35,
                           command=lambda: handle_login(user_email.get(), user_password.get()))
        register_btn = Button(root, text="open account", width=35,
                              command=handle_register)

        # text fields
        email_text = Text(root, )

        # add to window
        user_email.grid(row=1, column=3, columnspan=5, sticky=E+W)
        user_password.grid(row=2, column=3, columnspan=5, sticky=E+W)
        login_btn.grid(row=3, column=3, columnspan=5, sticky=E+W)
        register_btn.grid(row=4, column=3, columnspan=5)

        root.mainloop()


print("login window opened")
login = BANK_MANAGEMENT_LOGIN()
