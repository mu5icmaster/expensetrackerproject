import sqlite3
import tkinter
import ttkbootstrap as ttk
import ttkbootstrap.dialogs.dialogs as dialogs
from ttkbootstrap.tableview import Tableview

import Database
import Theme
from datetime import datetime, timedelta

class Dashboard():

    def __init__(self, root, Visuals, Credentials=None):

        # Class Attributes
        self.root = root
        self.Visuals = Visuals
        self.username = "Ruri"
        self.email = "raspberryruri@gmail.com"
        self.TotalBudget = tkinter.IntVar()
        self.TotalBudget.set(0)
        self.TotalBalance = tkinter.IntVar()
        self.TotalExpense = tkinter.IntVar()
        self.BalanceLeft = tkinter.IntVar()
        self.Counter = 1

        # Update the StringVar values if Credentials is provided
        if Credentials:
            self.username = Credentials.username.get()
            self.email = Credentials.email.get()

        # Creates TopLevel Window
        self.TopLevel = tkinter.Toplevel(self.root)
        self.TopLevel.title("ExpenseMate")
        self.TopLevel.columnconfigure(0, weight=1)
        self.TopLevel.columnconfigure(1, weight=5)
        self.TopLevel.rowconfigure(0, weight=1)
        self.TopLevel.rowconfigure(1, weight=5)

        # Creates Left Frame
        self.FrameW = ttk.Frame(self.TopLevel)
        self.FrameW.grid(column=0, row=0, rowspan=2, sticky="nwes")

        # ExpenseMate
        ttk.Label(self.FrameW, text="ExpenseMate", font=self.Visuals.BigText, anchor="center").grid(row=1, column=1,
                                                                                               sticky="nwes")

        # Separator
        ttk.Separator(self.FrameW).grid(row=2, column=1, sticky="nwe")

        # Username (Change)
        ttk.Label(self.FrameW, text=self.username, font=self.Visuals.BigText, anchor="center").grid(row=3, column=1,
                                                                                               sticky="wes")

        # Email (Change)
        ttk.Label(self.FrameW, text=self.email, font=self.Visuals.Text, anchor="center").grid(row=4, column=1, sticky="nwe")

        # Vertical Separator
        ttk.Separator(self.FrameW, orient="vertical").grid(row=1, column=2, rowspan=6, sticky="nes")

        # Resizing
        self.FrameW.rowconfigure(0, weight=0)
        self.FrameW.rowconfigure(1, weight=1)
        self.FrameW.rowconfigure(2, weight=1)
        self.FrameW.rowconfigure(3, weight=1)
        self.FrameW.rowconfigure(4, weight=1)
        self.FrameW.rowconfigure(5, weight=1)
        self.FrameW.rowconfigure(6, weight=1)
        self.FrameW.columnconfigure(1, weight=1)
        self.FrameW.columnconfigure(2, weight=0)

        # Creates Top Right Frame
        self.FrameNE = ttk.Frame(self.TopLevel, bootstyle="light")
        self.FrameNE.grid(column=1, row=0, sticky="nwes")

        # Creates Bottom Right Frame
        self.FrameSE = ttk.Frame(self.TopLevel, bootstyle="light")
        self.FrameSE.grid(column=1, row=1, sticky="nwes")

        self.TopLevel.bind("<Enter>", self.check_notification)

    def check_notification(self, *args):
        try:
            if self.BalanceLeft.get() >= 0:
                self.Counter = 1
            elif self.BalanceLeft.get() < 0 and self.Counter == 1:
                self.Counter = 0
                dialogs.Messagebox.ok(title="Warning", message="You have exceeded your total balance.",
                                      parent=self.TopLevel)


        except Exception as e:
            print(f"Error in check_notification: {e}")



    def Create_Expense(self):

        # Budget Button
        ttk.Button(self.FrameW, text="Budget", bootstyle="link", command=lambda: self.StartBudget()).grid(row=5, column=1)

        # Date
        current_date = datetime.now()
        ttk.Label(self.FrameNE,anchor="center", text= f"{current_date.strftime('%B %d')}", font=self.Visuals.BoldText, background=self.Visuals.Theme.colors.get("light")).grid(row=1, column=1, sticky="s")
        first_day = current_date.replace(day=1)
        last_day = (first_day.replace(month=first_day.month % 12 + 1, day=1) - timedelta(days=1))
        daterange = f"{first_day.strftime('%d')} - {last_day.strftime('%d %B, %Y')}"
        ttk.Label(self.FrameNE, text=daterange, font=self.Visuals.Text, background=self.Visuals.Theme.colors.get("light")).grid(row=2, column=1)

        # Expenses
        ttk.Label(self.FrameNE, text="Expenses", font=self.Visuals.BoldText, anchor="center", background=self.Visuals.Theme.colors.get("light")).grid(row=1, column=3, columnspan=3, sticky="swe")

        # Edit Expense Button
        ttk.Button(self.FrameNE, style="primary-outline", text="Edit Expense",
                   command=lambda: EditExpense(table, self)).grid(row=2, column=3)

        # Delete Expense Button
        ttk.Button(self.FrameNE, style="primary-outline", text="Delete Expense",
                   command=lambda: DeleteExpense(table, self)).grid(row=2, column=4)

        # Add Expense Button
        ttk.Button(self.FrameNE, style="primary-outline", text="Add Expense", command=lambda: AddExpense(self, table)).grid(row=2, column=5)

        self.FrameNE.rowconfigure(1, weight=1)
        self.FrameNE.rowconfigure(2, weight=1)
        self.FrameNE.columnconfigure(1, weight=1)
        self.FrameNE.columnconfigure(2, weight=4)
        self.FrameNE.columnconfigure(3, weight=1)
        self.FrameNE.columnconfigure(4, weight=0)
        self.FrameNE.columnconfigure(5, weight=1)

        # Creates Table

        coldata = [
            {"text": "ID No.", "anchor": "center", "stretch": True},
            {"text": "Date", "anchor": "center", "stretch": True},
            {"text": "Payee", "anchor": "center", "stretch": True},
            {"text": "Description", "anchor": "center", "stretch": True},
            {"text": "Amount", "anchor": "center", "stretch": True},
            {"text": "Mode of Payment", "anchor": "center", "stretch": True}
            ]

        rowdata=[]

        table = Tableview(
            master=self.FrameSE,
            coldata=coldata,
            rowdata=rowdata,
            searchable=True,
            autofit=True,
            autoalign=True,
            stripecolor=(self.Visuals.Theme.colors.get("light"), None),
            bootstyle="info"
        )

        # Removes default horizontal scrollbar and creates a vertical Scrollbar

        scrollbar = None
        for child in table.winfo_children():
            if type(child) == tkinter.ttk.Scrollbar and isinstance(child, tkinter.ttk.Scrollbar):
                scrollbar = child
            if type(child) == tkinter.ttk.Treeview and isinstance(child, tkinter.ttk.Treeview):
                parent = child

        scrollbar.forget()

        Scrollbar = ttk.Scrollbar(self.FrameSE, orient="vertical", command=parent.yview, bootstyle="rounded")
        table.configure(yscrollcommand=Scrollbar.set)

        table.grid(row=1, column=1, sticky="nwes", rowspan=2)
        Scrollbar.grid(row=1, column=2, sticky="nes", rowspan=2)

        UpdateTable(table, self)

        self.FrameSE.rowconfigure(1, weight=1)
        self.FrameSE.columnconfigure(1, weight=1)
        self.FrameSE.columnconfigure(2, weight=0)


    def Create_Budget(self):

        # Budget Button
        ttk.Button(self.FrameW, text="Expenses", bootstyle="link", command=lambda: self.StartExpense()).grid(row=5, column=1)

        # Date
        current_date = datetime.now()
        ttk.Label(self.FrameNE, anchor="center", text=f"{current_date.strftime('%B %d')}", font=self.Visuals.BoldText,
                  background=self.Visuals.Theme.colors.get("light")).grid(row=1, column=1, sticky="s")
        first_day = current_date.replace(day=1)
        last_day = (first_day.replace(month=first_day.month % 12 + 1, day=1) - timedelta(days=1))
        daterange = f"{first_day.strftime('%d')} - {last_day.strftime('%d %B, %Y')}"
        ttk.Label(self.FrameNE, text=daterange, font=self.Visuals.Text,
                  background=self.Visuals.Theme.colors.get("light")).grid(row=2, column=1)

        # Expenses
        ttk.Label(self.FrameNE, text="Budget", font=self.Visuals.BoldText, anchor="center",
                  background=self.Visuals.Theme.colors.get("light")).grid(row=1, column=3, columnspan=3, sticky="swe")

        # Add Balance Button
        ttk.Button(self.FrameNE, style="primary-outline", text="Add Balance",
                   command=lambda: AddBalance(self)).grid(row=2, column=3)

        # Add Budget Button
        ttk.Button(self.FrameNE, style="primary-outline", text="Add Budget",
                   command=lambda: AddBudget(self)).grid(row=2, column=4)

        # Reset Button
        ttk.Button(self.FrameNE, style="primary-outline", text="Reset",
                   command=lambda: Reset(self)).grid(row=2, column=5)

        # Frame 1 (top left frame)

        Frame1 = ttk.Frame(self.FrameSE, padding=20, bootstyle="default")
        Frame1.grid(row=1, column=1, sticky="nwes")
        Frame11 = ttk.Frame(Frame1, bootstyle="light")
        Frame11.grid(row=1, column=1, sticky="nwes")

        ttk.Label(Frame11, text="Total Budget", font=self.Visuals.BoldText,
                  background=self.Visuals.Theme.colors.get("light"), anchor="center").grid(row=1, column=1)
        ttk.Label(Frame11, textvariable=self.TotalBudget, font=self.Visuals.BigText,
                  background=self.Visuals.Theme.colors.get("light"), anchor="center").grid(row=2, column=1, sticky="n")

        Frame1.rowconfigure(1, weight=1)
        Frame1.columnconfigure(1, weight=1)
        Frame11.rowconfigure(1, weight=1)
        Frame11.rowconfigure(2, weight=1)
        Frame11.columnconfigure(1, weight=1)

        # Frame 2 (top right frame)
        Frame2 = ttk.Frame(self.FrameSE, padding=20, bootstyle="default")
        Frame2.grid(row=1, column=2, sticky="nwes")
        Frame21 = ttk.Frame(Frame2, bootstyle="light")
        Frame21.grid(row=1, column=1, sticky="nwes")

        ttk.Label(Frame21, text="Total Expenses", font=self.Visuals.BoldText,
                  background=self.Visuals.Theme.colors.get("light"), anchor="center").grid(row=1, column=1)
        ttk.Label(Frame21, textvariable=self.TotalExpense, font=self.Visuals.BigText,
                  background=self.Visuals.Theme.colors.get("light"), anchor="center").grid(row=2, column=1, sticky="n")

        Frame2.rowconfigure(1, weight=1)
        Frame2.columnconfigure(1, weight=1)
        Frame21.rowconfigure(1, weight=1)
        Frame21.rowconfigure(2, weight=1)
        Frame21.columnconfigure(1, weight=1)

        # Frame 3 (bottom left frame)
        Frame3 = ttk.Frame(self.FrameSE, padding=20, bootstyle="default")
        Frame3.grid(row=2, column=1, sticky="nwes")
        Frame31 = ttk.Frame(Frame3, bootstyle="light")
        Frame31.grid(row=1, column=1, sticky="nwes")

        ttk.Label(Frame31, text="Total Balance", font=self.Visuals.BoldText,
                  background=self.Visuals.Theme.colors.get("light"), anchor="center").grid(row=1, column=1)
        ttk.Label(Frame31, textvariable=self.TotalBalance, font=self.Visuals.BigText,
                  background=self.Visuals.Theme.colors.get("light"), anchor="center").grid(row=2, column=1, sticky="n")

        Frame3.rowconfigure(1, weight=1)
        Frame3.columnconfigure(1, weight=1)
        Frame31.rowconfigure(1, weight=1)
        Frame31.rowconfigure(2, weight=1)
        Frame31.columnconfigure(1, weight=1)

        # Frame 4 (bottom right frame)
        Frame4 = ttk.Frame(self.FrameSE, padding=20, bootstyle="default")
        Frame4.grid(row=2, column=2, sticky="nwes")
        Frame41 = ttk.Frame(Frame4, bootstyle="light")
        Frame41.grid(row=1, column=1, sticky="nwes")

        ttk.Label(Frame41, text="Balance Left", font=self.Visuals.BoldText,
                  background=self.Visuals.Theme.colors.get("light"), anchor="center").grid(row=1, column=1)
        ttk.Label(Frame41, textvariable=self.BalanceLeft, font=self.Visuals.BigText,
                  background=self.Visuals.Theme.colors.get("light"), anchor="center").grid(row=2, column=1, sticky="n")

        Frame4.rowconfigure(1, weight=1)
        Frame4.columnconfigure(1, weight=1)
        Frame41.rowconfigure(1, weight=1)
        Frame41.rowconfigure(2, weight=1)
        Frame41.columnconfigure(1, weight=1)

        Database.UpdateDashboardInfo(self)

        self.FrameNE.rowconfigure(1, weight=1)
        self.FrameNE.rowconfigure(2, weight=1)
        self.FrameNE.columnconfigure(1, weight=1)
        self.FrameNE.columnconfigure(2, weight=4)
        self.FrameNE.columnconfigure(3, weight=1)
        self.FrameNE.columnconfigure(4, weight=0)
        self.FrameNE.columnconfigure(5, weight=1)
        self.FrameNE.columnconfigure(6, weight=0)

        self.FrameSE.rowconfigure(1, weight=1)
        self.FrameSE.rowconfigure(2, weight=1)
        self.FrameSE.columnconfigure(1, weight=1)
        self.FrameSE.columnconfigure(2, weight=1)


    def StartExpense(self):
        self.DestroyWidgets(self.FrameNE)
        self.DestroyWidgets(self.FrameSE)
        self.FrameW.forget()
        self.Create_Expense()

    def StartBudget(self):
        self.DestroyWidgets(self.FrameNE)
        self.DestroyWidgets(self.FrameSE)
        self.FrameW.forget()
        self.Create_Budget()

    def DestroyWidgets(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

def UpdateTable(table, Dashboard):

    # Resets Table Rows
    table.delete_rows()

    # Fetches Data from Database
    with sqlite3.connect("ExpenseMate.db") as db:
        cursor = db.cursor()
        print(Dashboard.username)
        cursor.execute('SELECT userID FROM UserTable WHERE username = ?', (Dashboard.username,))
        userID = cursor.fetchone()[0]
        all_data = db.execute('SELECT * FROM ExpenseTracker WHERE userID = ?', (userID,))
        data = all_data.fetchall()

    # Inserts Data into Table
    for values in data:
        table.insert_row(values=values)

    # Refreshes Table
    table.load_table_data()


def AddExpense(Dashboard, table):
    # Create a Toplevel window for the pop-up
    popup = ttk.Toplevel(Dashboard.TopLevel)
    popup.title("Add Expense")

    # Make the pop-up window transient for the main window
    popup.transient(Dashboard.TopLevel)

    # Make the pop-up window grab the focus
    popup.grab_set()

    # StringVars for user inputs
    Values = [tkinter.StringVar() for i in range(5)]

    # Labels and Entries
    ttk.Label(popup, text="Date:").grid(row=0, column=0, padx=10, pady=5)
    date_entry = ttk.DateEntry(popup, firstweekday=0)
    date_entry.entry.configure(textvariable = Values[0])
    date_entry.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(popup, text="Payee:").grid(row=1, column=0, padx=10, pady=5)
    payee_entry = ttk.Entry(popup, textvariable=Values[1])
    payee_entry.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(popup, text="Description:").grid(row=2, column=0, padx=10, pady=5)
    description_entry = ttk.Entry(popup, textvariable=Values[2])
    description_entry.grid(row=2, column=1, padx=10, pady=5)

    ttk.Label(popup, text="Amount:").grid(row=3, column=0, padx=10, pady=5)
    amount_entry = ttk.Entry(popup, textvariable=Values[3])
    amount_entry.grid(row=3, column=1, padx=10, pady=5)

    ttk.Label(popup, text="Mode of Payment:").grid(row=4, column=0, padx=10, pady=5)
    payment_mode_entry = ttk.Combobox(popup, textvariable=Values[4], values=["Cash", "Credit Card", "Debit Card", "TNG E-Wallet"])
    Values[4].set("Select an item")
    payment_mode_entry.grid(row=4, column=1, padx=10, pady=5)

    payment_mode_entry.bind("<FocusOut>", lambda event, x=Values[4]:validate_input(event, x))

    def Submit(Values, popup, Dashboard):

        for _, values in enumerate(Values):
            if not values.get() or values.get() == "Select an item":
                dialogs.Messagebox.ok(title='Fields empty!', message="Please fill all the missing fields!", parent=popup)
                return

        try:
            Database.AddExpense(Values, Dashboard)
            dialogs.Messagebox.ok(title="Success!", message="Your expense has been recorded!", parent=popup)
            popup.destroy()
            UpdateTable(table, Dashboard)

        except:
            dialogs.Messagebox.ok(title="Error!", message="An unknown error has occurred.", parent=popup)
            popup.destroy()
            pass

    # Button to submit the form
    submit_button = ttk.Button(popup, text="Submit", command=lambda: Submit(Values, popup, Dashboard))
    submit_button.grid(row=5, column=1, pady=10)

    # Resizes
    popup.columnconfigure(0, weight=1)
    popup.columnconfigure(1, weight=1)
    popup.rowconfigure(0, weight=1)
    popup.rowconfigure(1, weight=1)
    popup.rowconfigure(2, weight=1)
    popup.rowconfigure(3, weight=1)
    popup.rowconfigure(4, weight=1)
    popup.rowconfigure(5, weight=1)

    # Wait for the pop-up window to be destroyed before allowing the main window to regain focus
    Dashboard.TopLevel.wait_window(popup)



def EditExpense(table, Dashboard):

    try:
        row = table.get_row(iid=table.view.selection()[0])
    except:
        dialogs.Messagebox.ok(title="Error", message="Please select an expense to edit.", parent=Dashboard.TopLevel)
        return

    # Create a Toplevel window for the pop-up
    popup = ttk.Toplevel(Dashboard.TopLevel)
    popup.title("Edit Expense")

    # Make the pop-up window transient for the main window
    popup.transient(Dashboard.TopLevel)

    # Make the pop-up window grab the focus
    popup.grab_set()

    # StringVars for user inputs
    Values = [tkinter.StringVar() for i in range(7)]

    for index, values in enumerate(row.values):
        Values[index].set(values)

    # Labels and Entries
    ttk.Label(popup, text="Date:").grid(row=0, column=0, padx=10, pady=5)
    date_entry = ttk.DateEntry(popup, firstweekday=0)
    date_entry.entry.configure(textvariable = Values[1])
    date_entry.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(popup, text="Payee:").grid(row=1, column=0, padx=10, pady=5)
    payee_entry = ttk.Entry(popup, textvariable= Values[2])
    payee_entry.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(popup, text="Description:").grid(row=2, column=0, padx=10, pady=5)
    description_entry = ttk.Entry(popup, textvariable= Values[3])
    description_entry.grid(row=2, column=1, padx=10, pady=5)

    ttk.Label(popup, text="Amount:").grid(row=3, column=0, padx=10, pady=5)
    amount_entry = ttk.Entry(popup, textvariable= Values[4])
    amount_entry.grid(row=3, column=1, padx=10, pady=5)

    ttk.Label(popup, text="Mode of Payment:").grid(row=4, column=0, padx=10, pady=5)
    payment_mode_entry = ttk.Combobox(popup, textvariable= Values[5], values=["Cash", "Credit Card", "Debit Card", "TNG E-Wallet"])
    payment_mode_entry.grid(row=4, column=1, padx=10, pady=5)

    payment_mode_entry.bind("<FocusOut>", lambda event, x=Values[5]: validate_input(event, x))

    def Submit(Values, popup, Dashboard):

        for _, values in enumerate(Values):
            if not values.get() or values.get() == "Select an item":
                dialogs.Messagebox.ok(title='Fields empty!', message="Please fill all the missing fields!", parent=popup)
                return

        try:
            Database.EditExpense(Values, Dashboard)
            dialogs.Messagebox.ok(title="Success!", message="Your expense has been edited!", parent=popup)
            popup.destroy()
            UpdateTable(table, Dashboard)

        except:
            dialogs.Messagebox.ok(title="Error!", message="An unknown error has occurred.", parent=popup)
            popup.destroy()
            pass

    # Button to submit the form
    submit_button = ttk.Button(popup, text="Submit", command=lambda: Submit(Values, popup, Dashboard))
    submit_button.grid(row=5, column=1, pady=10)

    # Resizes
    popup.columnconfigure(0, weight=1)
    popup.columnconfigure(1, weight=1)
    popup.rowconfigure(0, weight=1)
    popup.rowconfigure(1, weight=1)
    popup.rowconfigure(2, weight=1)
    popup.rowconfigure(3, weight=1)
    popup.rowconfigure(4, weight=1)
    popup.rowconfigure(5, weight=1)

    # Wait for the pop-up window to be destroyed before allowing the main window to regain focus
    Dashboard.TopLevel.wait_window(popup)


def DeleteExpense(table, Dashboard):

    try:
        row = table.get_row(iid=table.view.selection()[0])
    except:
        dialogs.Messagebox.ok(title="Error", message="Please select an expense to delete.", parent=Dashboard.TopLevel)
        return

    surety = dialogs.Messagebox.yesno(title="Delete expense?", message="Action cannot be undone.", parent=Dashboard.TopLevel)

    if surety == "Yes":
        Database.DeleteExpense(row.values, Dashboard)
        dialogs.Messagebox.ok(title='Success!', message='Your expense has been deleted!', parent=Dashboard.TopLevel)
        UpdateTable(table, Dashboard)


def AddBudget(Dashboard):
    # Create a Toplevel window for the pop-up
    popup = ttk.Toplevel(Dashboard.TopLevel)
    popup.title("Add Budget")

    # Make the pop-up window transient for the main window
    popup.transient(Dashboard.TopLevel)

    # Make the pop-up window grab the focus
    popup.grab_set()

    # StringVars for user inputs
    values = [tkinter.StringVar() for i in range(2)]
    values[1].set(Dashboard.username)

    # Label and Entry
    ttk.Label(popup, text="Budget:").grid(row=1, column=0, padx=10, pady=5)
    payee_entry = ttk.Entry(popup, textvariable=values[0])
    payee_entry.grid(row=1, column=1, padx=10, pady=5)

    def Submit(Values, popup, Dashboard):

        for _, values in enumerate(Values):
            if not values.get():
                dialogs.Messagebox.ok(title='Fields empty!', message="Please fill all the missing fields!", parent=popup)
                return

        try:
            Database.AddBudget(Values, Dashboard)
            dialogs.Messagebox.ok(title="Success!", message="Your budget has been added!", parent=popup)
            popup.destroy()

        except:
            dialogs.Messagebox.ok(title="Error!", message="An unknown error has occurred.", parent=popup)
            popup.destroy()
            pass


    # Button to submit the form
    submit_button = ttk.Button(popup, text="Submit",command=lambda: Submit(values, popup, Dashboard), bootstyle="info")
    submit_button.grid(row=2, column=0, pady=10, columnspan=2)

    # Resizes
    popup.columnconfigure(0, weight=1)
    popup.columnconfigure(1, weight=1)
    popup.rowconfigure(1, weight=1)
    popup.rowconfigure(2, weight=1)

    # Wait for the pop-up window to be destroyed before allowing the main window to regain focus
    Dashboard.TopLevel.wait_window(popup)

def AddBalance(Dashboard):
    # Create a Toplevel window for the pop-up
    popup = ttk.Toplevel(Dashboard.TopLevel)
    popup.title("Add Balance")

    # Make the pop-up window transient for the main window
    popup.transient(Dashboard.TopLevel)

    # Make the pop-up window grab the focus
    popup.grab_set()

    # StringVars for user inputs
    values = [tkinter.StringVar() for i in range(2)]
    values[1].set(Dashboard.username)

    # Label and Entry
    ttk.Label(popup, text="Balance:").grid(row=1, column=0, padx=10, pady=5)
    payee_entry = ttk.Entry(popup, textvariable=values[0])
    payee_entry.grid(row=1, column=1, padx=10, pady=5)

    def Submit(Values, popup, Dashboard):

        for _, values in enumerate(Values):
            if not values.get():
                dialogs.Messagebox.ok(title='Fields empty!', message="Please fill all the missing fields!", parent=popup)
                return

        try:
            Database.AddBalance(Values, Dashboard)
            dialogs.Messagebox.ok(title="Success!", message="Your balance has been added!", parent=popup)
            popup.destroy()

        except:
            dialogs.Messagebox.ok(title="Error!", message="An unknown error has occurred.", parent=popup)
            popup.destroy()
            pass

    # Button to submit the form
    submit_button = ttk.Button(popup, text="Submit",command=lambda:Submit(values, popup, Dashboard), bootstyle="info")
    submit_button.grid(row=2, column=0, pady=10, columnspan=2)

    # Resizes
    popup.columnconfigure(0, weight=1)
    popup.columnconfigure(1, weight=1)
    popup.rowconfigure(1, weight=1)
    popup.rowconfigure(2, weight=1)

    # Wait for the pop-up window to be destroyed before allowing the main window to regain focus
    Dashboard.TopLevel.wait_window(popup)

def Reset(Dashboard):
    surety = dialogs.Messagebox.yesno(title="Delete Budget?", message="Action cannot be undone.", parent=Dashboard.TopLevel)

    if surety == "Yes":
        Database.Reset(Dashboard)
        dialogs.Messagebox.ok(title='Success!', message='Your budget has been reset!', parent=Dashboard.TopLevel)

def validate_input(event, textvar):
    selected_item = textvar.get()

    if selected_item not in ["Cash", "Credit Card", "Debit Card", "TNG E-Wallet"]:
        textvar.set("Select an item")




if __name__ == "__main__":

    # Creates root window
    root = tkinter.Tk()
    root.withdraw()

    MainPage = Dashboard(root, Theme.Visuals(style="flatly"))
    MainPage.Create_Expense()
    #MainPage.Create_Budget()

    root.mainloop()