from tkinter import *
from tkinter import messagebox
from sympy import EX
import database
from decimal import Decimal
from authentication_gui_and_program import *

# login_page = Login()
# login_page.mainloop_window()


class BANK_MANAGEMENT:
    def __init__(self, user_id, root=Tk()):
        self.root = root
        root.title("Bank management")
        root.geometry('600x400')

        # get user information
        self.user_id = user_id
        db = database.DATABASE()
        self.user = db.findById(self.user_id).to_dict()
        self.balance = self.user['balance'][0]
        self.email = self.user['email'][0]

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

        self.frame2 = Frame(root, width=520, height=60)
        self.frame2.grid(row=1, columnspan=2,
                         padx=20, pady=10, sticky=E+W)

        self.deposit_btn = Button(
            self.frame2, text="deposit", width=18, command=self.deposit_ui)
        self.deposit_btn.grid(row=0, column=0, padx=3)

        self.withdraw_btn = Button(self.frame2, text="withdraw", width=18)
        self.withdraw_btn.grid(row=0, column=1)

        self.transfer_btn = Button(self.frame2, text="transfer", width=18)
        self.transfer_btn.grid(row=0, column=2)

        self.activity_btn = Button(self.frame2, text="activity", width=18)
        self.activity_btn.grid(row=0, column=3)

        self.frame3 = Frame(root, width=520)
        self.frame.grid(row=2, columnspan=2)

    def deposit_ui(self):
        self.deposit_window = Toplevel(self.root)
        self.deposit_window.geometry("410x300")
        self.deposit_window.title('Deposit')

        ui_frame = Frame(self.deposit_window)

        balance_label = Label(ui_frame,
                              text=f"${self.balance}", font=(42))
        amount_label = Label(ui_frame, text="Amount $")
        self.amount_entry = Entry(ui_frame)
        button = Button(ui_frame, text="send", command=self.handle_deposit)

        balance_label.grid(row=0, column=0, columnspan=2)
        amount_label.grid(row=1, column=0, sticky=W)
        self.amount_entry.grid(row=1, column=1)
        button.grid(row=2, columnspan=2)

        ui_frame.pack()

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

        if res:
            messagebox.showinfo(title="Success",
                                message="Amount has been deposited.")
            self.user = db.findById(self.user_id).to_dict()
            self.balance = self.user['balance'][0]
            self.balance_label.config(text=f"Balance: ${self.balance}")
            return

    def update_user_information(self, id):
        db = database.DATABASE()
        self.user = db.findById(self.user_id).to_dict()
        self.balance = self.user['balance'][0]

    def mainloop_root(self):
        self.root.mainloop()


main_win = BANK_MANAGEMENT(5)
# main_win = BANK_MANAGEMENT(login_page.user_id)
main_win.mainloop_root()
