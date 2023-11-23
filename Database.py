import sqlite3
import re
#from tkinter import messagebox as mb
import ttkbootstrap.dialogs.dialogs as mb
import Dashboard

# Initialise User Table
with sqlite3.connect("ExpenseMate.db") as db:
    UserTable = db.cursor()

    UserTable.execute('''
    CREATE TABLE IF NOT EXISTS UserTable(
    userID INTEGER PRIMARY KEY,
    username VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL,
    email_address VARCHAR(50) NOT NULL);
    ''')

    db.commit()

# Initialise Expenses Table
    Expenses = db.cursor()

    Expenses.execute(
      'CREATE TABLE IF NOT EXISTS ExpenseTracker '
      '(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, '
      'Date DATETIME, Payee TEXT, Description TEXT, Amount FLOAT, ModeOfPayment TEXT, userID INTEGER,'
      'FOREIGN KEY (userID) REFERENCES UserTable(userID))')

    db.commit()

    Budget = db.cursor()

    Budget.execute("""
    CREATE TABLE IF NOT EXISTS Budget (
        Budget_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Budget INT,
        Balance DECIMAL(10, 2),  
        User_ID INT,
        FOREIGN KEY (User_ID) REFERENCES UserTable(userID));
        """)

    db.commit()


def RegisterUser(Credentials):

    with sqlite3.connect("ExpenseMate.db") as db:
        cursor = db.cursor()

    find_user = ("SELECT * FROM UserTable WHERE username = ?")
    cursor.execute(find_user, [(Credentials.username.get())])

    if (cursor.fetchall()):
        Credentials.username_error_message.set("Username taken")
        return False

    insert = "INSERT INTO UserTable(username, password, email_address) VALUES(?,?,?)"
    cursor.execute(insert, [(Credentials.username.get()), (Credentials.password.get()), (Credentials.email.get())])
    db.commit()
    return True

def LoginUser(Credentials):

    with sqlite3.connect("ExpenseMate.db") as db:
        cursor = db.cursor()

    if re.match("^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$", Credentials.username.get()):
        statement = "SELECT username from UserTable WHERE email_address= ? AND password = ?"
        cursor.execute(statement, (Credentials.username.get(), Credentials.password.get()))

    else:
        statement = "SELECT username from UserTable WHERE username= ? AND password = ?"
        cursor.execute(statement, (Credentials.username.get(), Credentials.password.get()))

    if not cursor.fetchone():  # An empty result evaluates to False.
        return False

    else:
        if re.match("^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$", Credentials.username.get()):
            Credentials.email.set(Credentials.username.get())
            statement = "SELECT username from UserTable WHERE email_address= ? AND password = ?"
            cursor.execute(statement, (Credentials.username.get(), Credentials.password.get()))
            Credentials.username.set("%s" % cursor.fetchone())

        else:
            statement = "SELECT email_address from UserTable WHERE username= ? AND password = ?"
            cursor.execute(statement, (Credentials.username.get(), Credentials.password.get()))
            Credentials.email.set("%s" % cursor.fetchone())

        return True


def AddExpense(date_var, payee_var, description_var, amount_var, payment_mode_var, table, popup, Visuals, info):

    if not date_var.get() or not payee_var.get() or not description_var.get() or not amount_var.get() or not payment_mode_var.get():
        mb.Messagebox.ok(title='Fields empty!', message="Please fill all the missing fields before pressing the add button!", parent=popup)

    else:

        with sqlite3.connect("ExpenseMate.db") as db:
            cursor = db.cursor()

            cursor.execute("SELECT UserID FROM UserTable WHERE username = ?", (info.username,))
            userID = cursor.fetchone()[0]

            cursor.execute(
                'INSERT INTO ExpenseTracker (Date, Payee, Description, Amount, ModeOfPayment, userID) VALUES (?, ?, ?, ?, ?, ?)',
                # SQL code for inserting values
                (date_var.get(), payee_var.get(), description_var.get(), amount_var.get(), payment_mode_var.get(), userID)
                # Parameters to insert into the values in the SQL code
            )
            db.commit()

        popup.destroy()
        #Dashboard.UpdateTable(table, Visuals)
        UpdateDashboardInfo(info)



def EditExpense(date_var, payee_var, description_var, amount_var, payment_mode_var, table, popup, Visuals, id, info):

    if not date_var.get() or not payee_var.get() or not description_var.get() or not amount_var.get() or not payment_mode_var.get():
        #mb.Messagebox.ok(title='Fields empty!', message="Please fill all the missing fields before pressing the add button!", parent=popup)
        popup.destroy()

    else:

        with sqlite3.connect("ExpenseMate.db") as db:
            cursor = db.cursor()
            cursor.execute('UPDATE ExpenseTracker SET Date = ?, Payee = ?, Description = ?, Amount = ?, ModeOfPayment = ? WHERE ID = ?',
                   (date_var.get(), payee_var.get(), description_var.get(), amount_var.get(), payment_mode_var.get(), id))
            db.commit()

        popup.destroy()
        #mb.Messagebox.ok(title='Data edited', message='We have updated the data and stored in the database as you wanted', parent=popup)
        UpdateDashboardInfo(info)


def DeleteExpense(values_selected, info):
    with sqlite3.connect("ExpenseMate.db") as db:
        cursor = db.cursor()
        cursor.execute('DELETE FROM ExpenseTracker WHERE ID=%d' % values_selected[
        0])  # SQL code to remove data from ExpenseTracker Table
        db.commit()
        UpdateDashboardInfo(info)

def AddBudget(popup, budget, username, info):

    if not budget.get():
        mb.Messagebox.ok(title='Fields empty!', message="Please fill all the missing fields before pressing the add button!", parent=popup)

    else:
        budget=budget.get()

        with sqlite3.connect("ExpenseMate.db") as db:
            user_cursor = db.cursor()
            user_cursor.execute("SELECT userID FROM UserTable WHERE username = ?", (username,))
            userID = user_cursor.fetchone()
            userID = userID[0]

        with sqlite3.connect("ExpenseMate.db") as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO Budget (Budget, Balance, User_ID) VALUES (?, ?, ?)", (budget, 0.0, userID))
            db.commit()

        popup.destroy()
        UpdateDashboardInfo(info)
        #mb.Messagebox.ok(title='Data edited', message='Data successfully updated!', parent=popup)

def CollectTotalBudget(username):
    with sqlite3.connect("ExpenseMate.db") as db:
        user_cursor = db.cursor()
        user_cursor.execute("SELECT Budget FROM Budget WHERE username = ?", (username,))
        result = user_cursor.fetchone()
        result = result[0]
        """.config(text=f'{result:.2f}')"""


def AddBalance(popup, balance, username, info):
    if not balance.get():
        mb.Messagebox.ok(title='Fields empty!',
                         message="Please fill all the missing fields before pressing the add button!",
                         parent=popup)

    else:
        balance = balance.get()

        with sqlite3.connect("ExpenseMate.db") as user_db:
            user_cursor = user_db.cursor()
            user_cursor.execute("SELECT userID FROM UserTable WHERE username = ?", (username,))
            userID = user_cursor.fetchone()
            userID = userID[0]

        with sqlite3.connect("ExpenseMate.db") as budget_db:
            cursor = budget_db.cursor()
            cursor.execute("INSERT INTO Budget (Budget, Balance, User_ID) VALUES (?, ?, ?)", (0.0, balance, userID))
            budget_db.commit()

        popup.destroy()
        UpdateDashboardInfo(info)
        #mb.Messagebox.ok(title='Data edited', message='Data successfully updated!', parent=popup)

def UpdateDashboardInfo(Info):
    with sqlite3.connect("ExpenseMate.db") as db:
        cursor = db.cursor()
        username = Info.username

        cursor.execute("SELECT UserID FROM UserTable WHERE username = ?", (username,))
        userID = cursor.fetchone()

        cursor.execute("SELECT SUM(Budget) FROM Budget WHERE User_ID = ?", userID)
        Info.TotalBudget.set(cursor.fetchone()[0])
        try:
            Info.TotalBudget.get()
        except:
            Info.TotalBudget.set(0)

        cursor.execute("SELECT SUM(Balance) FROM Budget WHERE User_ID = ?", userID)
        Info.TotalBalance.set(cursor.fetchone()[0])
        try:
            Info.TotalBalance.get()
        except:
            Info.TotalBalance.set(0)

        cursor.execute("SELECT SUM(Amount) FROM ExpenseTracker WHERE userID = ?", userID)
        Info.TotalExpense.set(cursor.fetchone()[0])
        try:
            Info.TotalExpense.get()
        except:
            Info.TotalExpense.set(0)

        Info.BalanceLeft.set(Info.TotalBalance.get() - Info.TotalExpense.get())
