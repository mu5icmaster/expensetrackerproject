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


def AddExpense(Values, Dashboard):

    with sqlite3.connect("ExpenseMate.db") as db:
        cursor = db.cursor()

        cursor.execute("SELECT UserID FROM UserTable WHERE username = ?", (Dashboard.username,))
        userID = cursor.fetchone()[0]

        cursor.execute(
            'INSERT INTO ExpenseTracker (Date, Payee, Description, Amount, ModeOfPayment, userID) VALUES (?, ?, ?, ?, ?, ?)',
            tuple(Values[i].get() for i in range(5)) + (userID,))

        db.commit()

        UpdateDashboardInfo(Dashboard)



def EditExpense(Values, Dashboard):

    with sqlite3.connect("ExpenseMate.db") as db:
        cursor = db.cursor()
        cursor.execute('UPDATE ExpenseTracker SET Date = ?, Payee = ?, Description = ?, Amount = ?, ModeOfPayment = ? WHERE ID = ?',
               tuple(Values[i].get() for i in range(1,6)) + (Values[0].get(),))
        db.commit()

    UpdateDashboardInfo(Dashboard)


def DeleteExpense(values, Dashboard):
    with sqlite3.connect("ExpenseMate.db") as db:
        cursor = db.cursor()
        cursor.execute('DELETE FROM ExpenseTracker WHERE ID=%d' % values[
        0])  # SQL code to remove data from ExpenseTracker Table
        db.commit()
        UpdateDashboardInfo(Dashboard)

def AddBudget(values, Dashboard):

    with sqlite3.connect("ExpenseMate.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT userID FROM UserTable WHERE username = ?", (values[1].get(), ))
        userID = cursor.fetchone()[0]
        cursor.execute("INSERT INTO Budget (Budget, User_ID) VALUES (?, ?)", (values[0].get(), userID))
        db.commit()

    UpdateDashboardInfo(Dashboard)

def AddBalance(values, Dashboard):

    with sqlite3.connect("ExpenseMate.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT userID FROM UserTable WHERE username = ?", (values[1].get(),))
        userID = cursor.fetchone()[0]
        cursor.execute("INSERT INTO Budget (Balance, User_ID) VALUES (?, ?)", (values[0].get(), userID))
        db.commit()

    UpdateDashboardInfo(Dashboard)

def Reset(username):
    with sqlite3.connect("ExpenseMate.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT userID FROM UserTable WHERE username = ?", (username, ))
        userID = cursor.fetchone()[0]
        cursor.execute("DELETE FROM Budget WHERE user_ID = ?", (userID,))

def UpdateDashboardInfo(Dashboard):
    with sqlite3.connect("ExpenseMate.db") as db:
        cursor = db.cursor()
        username = Dashboard.username

        cursor.execute("SELECT UserID FROM UserTable WHERE username = ?", (username,))
        userID = cursor.fetchone()

        cursor.execute("SELECT SUM(Budget) FROM Budget WHERE User_ID = ?", userID)
        Dashboard.TotalBudget.set(cursor.fetchone()[0])
        try:
            Dashboard.TotalBudget.get()
        except:
            Dashboard.TotalBudget.set(0)

        cursor.execute("SELECT SUM(Balance) FROM Budget WHERE User_ID = ?", userID)
        Dashboard.TotalBalance.set(cursor.fetchone()[0])
        try:
            Dashboard.TotalBalance.get()
        except:
            Dashboard.TotalBalance.set(0)

        cursor.execute("SELECT SUM(Amount) FROM ExpenseTracker WHERE userID = ?", userID)
        Dashboard.TotalExpense.set(cursor.fetchone()[0])
        try:
            Dashboard.TotalExpense.get()
        except:
            Dashboard.TotalExpense.set(0)

        Dashboard.BalanceLeft.set(Dashboard.TotalBalance.get() - Dashboard.TotalExpense.get())
