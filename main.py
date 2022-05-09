from tkinter import *
from tkinter import messagebox
from sympy import EX
import database
from decimal import Decimal
from authentication_gui_and_program import *

login_page = Login()
login_page.mainloop_window()


class BANK_MANAGEMENT:
    """
    BANK_MANAGEMENT definition builds the user interface and logic for the main bank system.
    The class initializes a Tk window as root, and accepts a user id received from the
    the authentication class to find the user and display the user's information.
    """

    def __init__(self, user_id, root=Tk()):
        # initialize tk widgets
        self.root = root
        root.title("Bank management")
        root.geometry('600x400')

        # get user information from database
        self.user_id = user_id
        db = database.DATABASE()
        self.user = db.findById(self.user_id).to_dict()
        self.balance = self.user['balance'][0]
        self.email = self.user['email'][0]

        # frame1 components
        self.frame1 = LabelFrame(root, width=520, height=100, padx=10, pady=10)
        self.frame1.grid(row=0, column=0, columnspan=2,
                         padx=20, pady=10, ipadx=20, sticky=E+W)

        self.logo_label = Label(self.frame1, text="Bank Management", font=(48))
        self.logo_label.place(relx=.04, rely=.35)

        self.user_email_label = Label(
            self.frame1, text=f"email: {self.email}")
        self.user_email_label.place(relx=.70, rely=.15)

        self.balance_label = Label(
            self.frame1, text=f"Balance: ${self.balance}")
        self.balance_label.place(relx=.70, rely=.45)

        # frame2 components
        self.frame2 = Frame(root, width=520, height=60)
        self.frame2.grid(row=1, columnspan=2,
                         padx=20, pady=10, sticky=E+W)

        self.deposit_btn = Button(
            self.frame2, text="deposit", width=18, command=self.deposit_ui)
        self.deposit_btn.grid(row=0, column=0, padx=3)

        self.withdraw_btn = Button(
            self.frame2, text="withdraw", width=18, command=self.withdraw_ui)
        self.withdraw_btn.grid(row=0, column=1)

        self.transfer_btn = Button(self.frame2, text="transfer", width=18)
        self.transfer_btn.grid(row=0, column=2)

        self.activity_btn = Button(self.frame2, text="activity", width=18)
        self.activity_btn.grid(row=0, column=3)

        # frame3 components
        self.frame3 = LabelFrame(root, width=520, height=60, padx=10, pady=10)
        self.frame3_container = Scrollbar(self.frame3, orient='vertical')
        self.frame3_container.pack(side=RIGHT)
        label = Label(self.frame3_container, text="hello").pack()
        label = Label(self.frame3_container, text="hello").pack()
        label = Label(self.frame3_container, text="hello").pack()
        label = Label(self.frame3_container, text="hello").pack()

        self.frame3.grid(row=2, column=0, columnspan=2,
                         padx=20, pady=10, ipadx=20, sticky=E+W)

    def frame3_components(self):
        pass

    def deposit_ui(self):
        # this function creates a top level tk window and prompts user to desposit
        # an amount into the user's account
        self.deposit_window = Toplevel(self.root)
        self.deposit_window.geometry("410x300")
        self.deposit_window.title('Deposit')

        # frame holds all widgets
        ui_frame = Frame(self.deposit_window)

        balance_label = Label(ui_frame,
                              text=f"${self.balance}", font=(42))
        amount_label = Label(ui_frame, text="Amount $")
        self.amount_entry = Entry(ui_frame)
        button = Button(ui_frame, text="send", command=self.handle_deposit)

        # display in frame
        balance_label.grid(row=0, column=0, columnspan=2)
        amount_label.grid(row=1, column=0, sticky=W)
        self.amount_entry.grid(row=1, column=1)
        button.grid(row=2, columnspan=2)

        # display frame
        ui_frame.pack()

    def withdraw_ui(self):
        # this function creates a top level tk window and prompts user to
        # take money out of user's account

        # create top level window
        self.withdraw_window = Toplevel(self.root)
        self.withdraw_window.geometry("410x300")
        self.withdraw_window.title('Withdraw')

        # holds all widgets
        ui_frame = Frame(self.withdraw_window)

        balance_label = Label(ui_frame,
                              text=f"${self.balance}", font=(42))
        amount_label = Label(ui_frame, text="Amount $")
        self.amount_entry = Entry(ui_frame)
        button = Button(ui_frame, text="send", command=self.handle_withdrawal)

        balance_label.grid(row=0, column=0, columnspan=2)
        amount_label.grid(row=1, column=0, sticky=W)
        self.amount_entry.grid(row=1, column=1)
        button.grid(row=2, columnspan=2)

        ui_frame.pack()

    def handle_withdrawal(self):
        # this function validates the amount to be taken out of the
        # users account, and pushes the changes to the database.
        try:
            amount = Decimal(f"-{self.amount_entry.get()}")
        except Exception as e:
            messagebox.showwarning(title="Amount error",
                                   message="Please enter a number.")
            return
        if not amount:
            messagebox.showwarning(title="Amount error",
                                   message="Please enter an amount.")
            return

        # connect to database
        db = database.DATABASE()
        res = db.depositToAccount(self.user_id, amount)
        db.add_transaction_record(self.user_id, amount)

        # check if data is saved to the database
        if res:
            messagebox.showinfo(title="Success",
                                message="Amount has been deposited.")
            self.user = db.findById(self.user_id).to_dict()
            self.balance = self.user['balance'][0]
            self.balance_label.config(text=f"Balance: ${self.balance}")
            self.deposit_window.destroy()
            return

    def handle_deposit(self):
        try:
            amount = Decimal(self.amount_entry.get())
        except Exception as e:
            messagebox.showwarning(title="Amount error",
                                   message="Please enter a number.")
            return

        if not amount:
            messagebox.showwarning(title="Amount error",
                                   message="Please enter an amount.")
            return

        if amount <= 0:
            messagebox.showwarning(title="Amount error",
                                   message="Amount must be greater than 0.")
            return

        db = database.DATABASE()
        res = db.depositToAccount(self.user_id, amount)
        db.add_transaction_record(self.user_id, amount)
        print(db.query('SELECT * FROM transactions'))
        if res:
            messagebox.showinfo(title="Success",
                                message="Amount has been deposited.")
            self.user = db.findById(self.user_id).to_dict()
            self.balance = self.user['balance'][0]
            self.balance_label.config(text=f"Balance: ${self.balance}")
            self.deposit_window.destroy()
            return

    def update_user_information(self, id):
        db = database.DATABASE()
        self.user = db.findById(self.user_id).to_dict()
        self.balance = self.user['balance'][0]

    def mainloop_root(self):
        self.root.mainloop()


# main_win = BANK_MANAGEMENT(1002)
main_win = BANK_MANAGEMENT(login_page.user_id)
main_win.mainloop_root()


# create a row for each record - transaction UI
# label -> anchor=W, relief=SUNKEN

# for entry in all transactions
#   long_string += entry
# label(long_strin)
