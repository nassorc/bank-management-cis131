from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from sympy import EX
import database
from decimal import Decimal
import pandas as pd
from authentication_gui_and_program import *
import datetime

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
        root.geometry('600x600')

        # get user information from database
        self.user_id = user_id
        db = database.DATABASE()
        self.user = db.findById(self.user_id).to_dict()
        self.balance = self.user['balance'][0]
        self.email = self.user['email'][0]

        # frame1 components
        frame1 = LabelFrame(root, width=520, height=100, padx=10, pady=10)
        frame1.grid(row=0, column=0, columnspan=2,
                    padx=20, pady=10, ipadx=20, sticky=E+W)

        logo_label = Label(frame1, text="Bank Management", font=(48))
        logo_label.place(relx=.04, rely=.35)

        self.user_email_label = Label(
            frame1, text=f"email: {self.email}")
        self.user_email_label.place(relx=.70, rely=.15)

        self.balance_label = Label(
            frame1, text=f"Balance: ${self.balance}")
        self.balance_label.place(relx=.70, rely=.45)

        # frame2 components
        frame2 = Frame(root, width=520, height=60)
        frame2.grid(row=1, columnspan=2,
                    padx=20, pady=10, sticky=E+W)

        deposit_btn = Button(
            frame2, text="deposit", width=18, command=self.deposit_ui)
        deposit_btn.grid(row=0, column=0, padx=3)

        withdraw_btn = Button(
            frame2, text="withdraw", width=18, command=self.withdraw_ui)
        withdraw_btn.grid(row=0, column=1)

        transfer_btn = Button(frame2, text="transfer",
                              width=18, command=self.transfer_ui)
        transfer_btn.grid(row=0, column=2)

        activity_btn = Button(frame2, text="Logout",
                              width=18, command=lambda: self.root.quit())
        activity_btn.grid(row=0, column=3)

        self.frame3 = Frame(root, width=520, height=40, padx=10, pady=10)
        self.create_record_ui()
        self.frame3.grid(row=2)

    def create_record_ui(self):
        self.record_frame = Frame(self.frame3)
        db = database.DATABASE()
        all_transactions = db.query(f"""SELECT account_id, amount, dt from transactions
                                        WHERE account_id = {self.user_id} ORDER BY dt DESC""").to_dict()
        date_exists = {}
        for i in range(len(all_transactions['account_id'])):
            amount = all_transactions['amount'][i]
            date = all_transactions['dt'][i].split()[0]
            amount_label = Label(self.record_frame, text=f"Deposit: ${amount}") if \
                (amount >= 0) else Label(self.record_frame, text=f"Withdrawal: ${abs(amount)}")
            date_label = Label(self.record_frame, text=f"{date}", bg='grey')

            if date not in date_exists:
                date_exists[date] = True
                date_label.pack()
                amount_label.pack()
            amount_label.pack()

        self.record_frame.pack()

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
        button = Button(ui_frame, text="send", command=self.make_deposit)

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
        # justify widgets center
        widget_container = Frame(self.withdraw_window)

        balance_label = Label(widget_container,
                              text=f"${self.balance}", font=(42))
        amount_label = Label(widget_container, text="Amount $")
        self.amount_entry = Entry(widget_container)
        button = Button(widget_container, text="send",
                        command=self.make_withdrawal)

        balance_label.grid(row=0, column=0, columnspan=2)
        amount_label.grid(row=1, column=0, sticky=W)
        self.amount_entry.grid(row=1, column=1)
        button.grid(row=2, columnspan=2)

        widget_container.pack()

    def transfer_ui(self):
        self.transfer_window = Toplevel(self.root)
        self.transfer_window.geometry("410x300")
        self.transfer_window.title('Transfer money')

        widget_container = Frame(self.transfer_window)

        # labels
        header_label = Label(widget_container, text="Transfer money")
        from_label = Label(widget_container, text="From: ")
        from_label_user = Label(
            widget_container, text=f"{self.email}", relief=SUNKEN)
        to_label = Label(widget_container, text="To: ")

        # entry
        self.amount = Entry(widget_container)
        self.transfer_to_email = Entry(widget_container)

        # button
        transfer_button = Button(
            widget_container, text="Transfer", command=self.make_transfer)

        # place on screen
        header_label.grid(row=0, column=0, columnspan=2)
        self.amount.grid(row=1, column=0, columnspan=2)
        from_label.grid(row=2, column=0, columnspan=2)
        from_label_user.grid(row=2, column=1, columnspan=2)
        to_label.grid(row=3, column=0, columnspan=2)
        self.transfer_to_email.grid(row=3, column=1, columnspan=2)
        transfer_button.grid(row=4, column=0, columnspan=2)

        widget_container.pack()

    def make_transfer(self):
        if not self.amount.get():
            messagebox.showwarning(title="Amount error",
                                   message="Input cannot be empty")
            return
        try:
            amount = Decimal(f"{self.amount.get()}")
        except Exception as e:
            messagebox.showwarning(title="Amount error",
                                   message="Please enter a number.")
            return
        if amount > self.balance:
            messagebox.showwarning(title="Amount error",
                                   message="insufficient funds.")
            return
        if amount <= 0:
            messagebox.showwarning(title="Amount error",
                                   message="Amount must be greater than 0.")
            return
        # connect to db
        db = database.DATABASE()
        user = db.findByEmail(self.transfer_to_email.get())

        if len(user) <= 0:
            messagebox.showwarning(title="email error",
                                   message="User does not exist.")
            return

        receiver_id = user.to_dict()['id'][0]

        # desposit to receiver
        res = db.deposit_to_Account(receiver_id, amount)

        # withdraw from sender
        withdraw_from_sender = db.withdraw_from_Account(
            self.user_id, Decimal(f'-{amount}'))

        if res and withdraw_from_sender:
            db.add_transfer_record(receiver_id, self.user_id, amount)
            messagebox.showinfo(title="Success",
                                message="The money has been sent")
            self.user = db.findById(self.user_id).to_dict()
            self.balance = self.user['balance'][0]
            self.balance_label.config(text=f"Balance: ${self.balance}")
            self.record_frame.destroy()
            self.create_record_ui()
            self.frame3.update()
            self.transfer_window.destroy()
            return
        messagebox.showwarning(title="Transfer failed",
                               message="Transfer failed")

    def make_withdrawal(self):
        # this function validates the amount to be taken out of the
        # users account, and pushes the changes to the database.
        if not self.amount_entry.get():
            messagebox.showwarning(title="Amount error",
                                   message="Input cannot be empty")
            return
        try:
            amount = Decimal(f"-{self.amount_entry.get()}")
        except Exception as e:
            messagebox.showwarning(title="Amount error",
                                   message="Please enter a number.")
            return
        if amount > self.balance:
            messagebox.showwarning(title="Amount error",
                                   message="insufficient funds.")
            return

        # connect to database
        db = database.DATABASE()
        res = db.withdraw_from_Account(self.user_id, amount)

        # check if data is saved to the database
        if res:
            messagebox.showinfo(title="Success",
                                message="Amount has been withdrawn.")
            self.user = db.findById(self.user_id).to_dict()
            self.balance = self.user['balance'][0]
            self.balance_label.config(text=f"Balance: ${self.balance}")
            self.record_frame.destroy()
            self.create_record_ui()
            self.frame3.update()
            self.withdraw_window.destroy()
            return
        messagebox.showwarning(title="Withdrawal failed",
                               message="Withdrawal failed")

    def make_deposit(self):
        if not self.amount_entry.get():
            messagebox.showwarning(title="Amount error",
                                   message="Input cannot be empty")
            return
        try:
            amount = Decimal(self.amount_entry.get())
        except Exception as e:
            messagebox.showwarning(title="Amount error",
                                   message="Please enter a number.")
            return
        if amount <= 0:
            messagebox.showwarning(title="Amount error",
                                   message="Amount must be greater than 0.")
            return

        db = database.DATABASE()
        res = db.deposit_to_Account(self.user_id, amount)
        if res:
            messagebox.showinfo(title="Success",
                                message="Amount has been deposited.")
            self.user = db.findById(self.user_id).to_dict()
            self.balance = self.user['balance'][0]
            self.balance_label.config(text=f"Balance: ${self.balance}")
            self.record_frame.destroy()
            self.create_record_ui()
            self.frame3.update()
            self.deposit_window.destroy()
            return

        messagebox.showwarning(title="Deposit failed",
                               message="Deposit failed")

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
