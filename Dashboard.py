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
                   command=lambda: EditExpense(self.TopLevel, table, self.Visuals, self)).grid(row=2, column=3)

        # Delete Expense Button
        ttk.Button(self.FrameNE, style="primary-outline", text="Delete Expense",
                   command=lambda: DeleteExpense(table, self.Visuals, self.TopLevel, self)).grid(row=2, column=4)

        # Add Expense Button
        ttk.Button(self.FrameNE, style="primary-outline", text="Add Expense", command=lambda: AddExpense(self.TopLevel, table, self.Visuals, self)).grid(row=2, column=5)

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
        print(table.winfo_children())
        for child in table.winfo_children():
            if type(child) == tkinter.ttk.Scrollbar and isinstance(child, tkinter.ttk.Scrollbar):
                scrollbar = child
            if type(child) == tkinter.ttk.Treeview and isinstance(child, tkinter.ttk.Treeview):
                parent = child

        scrollbar.forget()

        Scrollbar = ttk.Scrollbar(self.FrameSE, orient="vertical", command=parent.yview, bootstyle="rounded")
        table.configure(yscrollcommand=Scrollbar.set)

        table.grid(row=1, column=1, sticky="nwes")
        Scrollbar.grid(row=1, column=2, sticky="nes")

        UpdateTable(table)

        self.FrameSE.rowconfigure(1, weight=1)
        self.FrameSE.columnconfigure(1, weight=1)
        self.FrameSE.columnconfigure(2, weight=0)

        #UpdateTable(table, self.Visuals)

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
                  background=self.Visuals.Theme.colors.get("light")).grid(row=1, column=3, columnspan=2, sticky="swe")

        # Add Balance Button
        ttk.Button(self.FrameNE, style="primary-outline", text="Add Balance",
                   command=lambda: AddBalance(self.TopLevel, table, self.username, self)).grid(row=2, column=3)

        # Add Budget Button
        ttk.Button(self.FrameNE, style="primary-outline", text="Add Budget",
                   command=lambda: AddBudget(self.TopLevel, table, self.username, self)).grid(row=2, column=4)

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

        """
        # Labels for Total Expense, Total Budget, Total Balance, and Total Balance Left
        ttk.Label(self.FrameSE, text="Total Expense:", font=self.Visuals.Text,background=self.Visuals.Theme.colors.get("light")).grid(row=1, column=2, sticky="nsew")
        ttk.Label(self.FrameSE, text="Total Budget:", font=self.Visuals.Text,background=self.Visuals.Theme.colors.get("light")).grid(row=1, column=1, sticky="nsew")
        ttk.Label(self.FrameSE, text="Total Balance:", font=self.Visuals.Text,background=self.Visuals.Theme.colors.get("light")).grid(row=2, column=1, sticky="nsew")
        ttk.Label(self.FrameSE, text="Total Balance Left:", font=self.Visuals.Text,background=self.Visuals.Theme.colors.get("light")).grid(row=2, column=2, sticky="nsew")

        # Display the values in labels
        ttk.Label(self.FrameSE, text="0.0", font=self.Visuals.Text, background=self.Visuals.Theme.colors.get("light")).grid(row=1, column=2, sticky="w")
        ttk.Label(self.FrameSE, text="0.0", font=self.Visuals.Text, background=self.Visuals.Theme.colors.get("light")).grid(row=1, column=1, sticky="w")
        ttk.Label(self.FrameSE, text="0.0", font=self.Visuals.Text, background=self.Visuals.Theme.colors.get("light")).grid(row=2, column=1, sticky="w")
        ttk.Label(self.FrameSE, text="0.0", font=self.Visuals.Text, background=self.Visuals.Theme.colors.get("light")).grid(row=2, column=2, sticky="w")
        """


        self.FrameNE.rowconfigure(1, weight=1)
        self.FrameNE.rowconfigure(2, weight=1)
        self.FrameNE.columnconfigure(1, weight=1)
        self.FrameNE.columnconfigure(2, weight=4)
        self.FrameNE.columnconfigure(3, weight=1)
        self.FrameNE.columnconfigure(4, weight=1)
        self.FrameNE.columnconfigure(5, weight=0)


        table = Tableview(
            master=self.FrameSE,
            autofit=True,
            autoalign=True,
            stripecolor=(self.Visuals.Theme.colors.get("light"), None),
            bootstyle="info"
        )

        #table.grid(row=1, column=1, sticky="nwes") Jet How ditched my table :(

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

def UpdateTable(table):

    # Resets Table Rows
    table.delete_rows()

    # Fetches Data from Database
    with sqlite3.connect("ExpenseMate.db") as db:
        all_data = db.execute('SELECT * FROM ExpenseTracker')
    data = all_data.fetchall()

    # Inserts Data into Table
    for values in data:
        table.insert_row(values=values)

    # Refreshes Table
    table.load_table_data()


def AddExpense(master, table, Visuals, info):
    # Create a Toplevel window for the pop-up
    popup = ttk.Toplevel(master)
    popup.title("Add Expense")

    # Make the pop-up window transient for the main window
    popup.transient(master)

    # Make the pop-up window grab the focus
    popup.grab_set()

    # StringVars for user inputs
    date_var = tkinter.StringVar()
    payee_var = tkinter.StringVar()
    description_var = tkinter.StringVar()
    amount_var = tkinter.StringVar()
    payment_mode_var = tkinter.StringVar()

    # Labels and Entries
    ttk.Label(popup, text="Date:").grid(row=0, column=0, padx=10, pady=5)
    date_entry = ttk.DateEntry(popup, firstweekday=0)
    date_entry.entry.configure(textvariable = date_var)
    date_entry.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(popup, text="Payee:").grid(row=1, column=0, padx=10, pady=5)
    payee_entry = ttk.Entry(popup, textvariable=payee_var)
    payee_entry.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(popup, text="Description:").grid(row=2, column=0, padx=10, pady=5)
    description_entry = ttk.Entry(popup, textvariable=description_var)
    description_entry.grid(row=2, column=1, padx=10, pady=5)

    ttk.Label(popup, text="Amount:").grid(row=3, column=0, padx=10, pady=5)
    amount_entry = ttk.Entry(popup, textvariable=amount_var)
    amount_entry.grid(row=3, column=1, padx=10, pady=5)

    ttk.Label(popup, text="Mode of Payment:").grid(row=4, column=0, padx=10, pady=5)
    payment_mode_entry = ttk.Combobox(popup, textvariable=payment_mode_var, values=["Cash", "Credit Card", "Debit Card", "TNG E-Wallet"])
    payment_mode_entry.set("Select an item")
    payment_mode_entry.grid(row=4, column=1, padx=10, pady=5)

    payment_mode_entry.bind("<FocusOut>", lambda event, x=payment_mode_var:validate_input(event, x))

    # Button to submit the form
    submit_button = ttk.Button(popup, text="Submit", command=lambda: Database.AddExpense(date_var, payee_var, description_var, amount_var, payment_mode_var, table, popup, Visuals, info))
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
    master.wait_window(popup)

    UpdateTable(table)

def EditExpense(master, table, Visuals, info):

    try:
        row = table.get_row(iid=table.view.selection()[0])
    except:
        dialogs.Messagebox.ok(title="Error", message="Please select an expense to edit.", parent=master)
        return

    print(row.values)

    # Create a Toplevel window for the pop-up
    popup = ttk.Toplevel(master)
    popup.title("Edit Expense")

    # Make the pop-up window transient for the main window
    popup.transient(master)

    # Make the pop-up window grab the focus
    popup.grab_set()

    # StringVars for user inputs
    id = row.values[0]
    date_var = tkinter.StringVar(value=row.values[1])
    payee_var = tkinter.StringVar(value=row.values[2])
    description_var = tkinter.StringVar(value=row.values[3])
    amount_var = tkinter.StringVar(value=row.values[4])
    payment_mode_var = tkinter.StringVar(value=row.values[5])

    # Labels and Entries
    ttk.Label(popup, text="Date:").grid(row=0, column=0, padx=10, pady=5)
    date_entry = ttk.DateEntry(popup, firstweekday=0)
    date_entry.entry.configure(textvariable = date_var)
    date_entry.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(popup, text="Payee:").grid(row=1, column=0, padx=10, pady=5)
    payee_entry = ttk.Entry(popup, textvariable=payee_var)
    payee_entry.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(popup, text="Description:").grid(row=2, column=0, padx=10, pady=5)
    description_entry = ttk.Entry(popup, textvariable=description_var)
    description_entry.grid(row=2, column=1, padx=10, pady=5)

    ttk.Label(popup, text="Amount:").grid(row=3, column=0, padx=10, pady=5)
    amount_entry = ttk.Entry(popup, textvariable=amount_var)
    amount_entry.grid(row=3, column=1, padx=10, pady=5)

    ttk.Label(popup, text="Mode of Payment:").grid(row=4, column=0, padx=10, pady=5)
    payment_mode_entry = ttk.Combobox(popup, textvariable=payment_mode_var, values=["Cash", "Credit Card", "Debit Card", "TNG E-Wallet"])
    payment_mode_entry.grid(row=4, column=1, padx=10, pady=5)

    payment_mode_entry.bind("<FocusOut>", lambda event, x=payment_mode_var:validate_input(event, x))

    # Button to submit the form
    submit_button = ttk.Button(popup, text="Submit", command=lambda: Database.EditExpense(date_var, payee_var, description_var, amount_var, payment_mode_var, table, popup, Visuals, id, info))
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
    master.wait_window(popup)

    UpdateTable(table)

def DeleteExpense(table, Visuals, parent, info):

    try:
        row = table.get_row(iid=table.view.selection()[0])
    except:
        dialogs.Messagebox.ok(title="Error", message="Please select an expense to delete.", parent=parent)
        return

    surety = dialogs.Messagebox.yesno(title="Delete expense?", message="Action cannot be undone.", parent=parent)

    if surety == "Yes":
        Database.DeleteExpense(row.values, info)
        dialogs.Messagebox.ok(title='Record deleted!',
                              message='The record you wanted to delete has been deleted successfully', parent=parent)
    UpdateTable(table)


def AddBudget(master, table, username, info):
    # Create a Toplevel window for the pop-up
    popup = ttk.Toplevel(master)
    popup.title("Add Budget")

    # Make the pop-up window transient for the main window
    popup.transient(master)

    # Make the pop-up window grab the focus
    popup.grab_set()

    # StringVars for user inputs
    budget_var = tkinter.StringVar()

    # Label and Entry
    ttk.Label(popup, text="Budget:").grid(row=1, column=0, padx=10, pady=5)
    payee_entry = ttk.Entry(popup, textvariable=budget_var)
    payee_entry.grid(row=1, column=1, padx=10, pady=5)

    # Button to submit the form
    submit_button = ttk.Button(popup, text="Submit",command=lambda: Database.AddBudget(popup, budget_var, username, info), bootstyle="info")
    submit_button.grid(row=2, column=0, pady=10, columnspan=2)

    # Resizes
    popup.columnconfigure(0, weight=1)
    popup.columnconfigure(1, weight=1)
    popup.rowconfigure(1, weight=1)
    popup.rowconfigure(2, weight=1)

    # Wait for the pop-up window to be destroyed before allowing the main window to regain focus
    master.wait_window(popup)

def AddBalance(master, table, username, info):
    # Create a Toplevel window for the pop-up
    popup = ttk.Toplevel(master)
    popup.title("Add Balance")

    # Make the pop-up window transient for the main window
    popup.transient(master)

    # Make the pop-up window grab the focus
    popup.grab_set()

    # StringVars for user inputs
    balance_var = tkinter.StringVar()

    # Label and Entry
    ttk.Label(popup, text="Balance:").grid(row=1, column=0, padx=10, pady=5)
    payee_entry = ttk.Entry(popup, textvariable=balance_var)
    payee_entry.grid(row=1, column=1, padx=10, pady=5)

    # Button to submit the form
    submit_button = ttk.Button(popup, text="Submit",command=lambda: Database.AddBalance(popup, balance_var, username, info), bootstyle="info")
    submit_button.grid(row=2, column=0, pady=10, columnspan=2)

    # Resizes
    popup.columnconfigure(0, weight=1)
    popup.columnconfigure(1, weight=1)
    popup.rowconfigure(1, weight=1)
    popup.rowconfigure(2, weight=1)

    # Wait for the pop-up window to be destroyed before allowing the main window to regain focus
    master.wait_window(popup)

def validate_input(event, textvar):
    selected_item = textvar.get()

    if selected_item not in ["Cash", "Credit Card", "Debit Card", "TNG E-Wallet"]:
        textvar.set("Select an item")




if __name__ == "__main__":

    # Creates root window
    root = tkinter.Tk()
    root.withdraw()

    MainPage = Dashboard(root, Theme.Visuals(style="flatly"))
    #MainPage.Create_Expense()
    MainPage.Create_Budget()

    root.mainloop()