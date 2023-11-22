import tkinter
import ttkbootstrap.dialogs.dialogs as dialogs
import ttkbootstrap as ttk
import ttkbootstrap.validation as validate
import Database
import Dashboard
import re

# Stores user credentials temporarily for verification
class Credentials():

    def __init__(self):
        self.email = tkinter.StringVar()
        self.email_error_message = tkinter.StringVar()
        self.username = tkinter.StringVar()
        self.username_error_message = tkinter.StringVar()
        self.password = tkinter.StringVar()
        self.password_error_message = tkinter.StringVar()
        self.image = tkinter.PhotoImage(file='Graphics/1.png')

    def Validate_Username(self, event):

        if event.postchangetext == "":
            self.username_error_message.set("")
            button["username"] = 0
            return True

        elif re.search("[^A-Za-z0-9-_\s]", event.postchangetext) is not None:
            self.username_error_message.set("Only alphanumeric symbols are allowed")
            button["username"] = 0
            return False

        else:
            self.username_error_message.set("")
            button["username"] = 1
            return True

    def Validate_Email(self, event):

        if event.postchangetext == "":
            self.email_error_message.set("")
            button["email"] = 0
            return True

        elif re.match("^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$", event.postchangetext):
            self.email_error_message.set("")
            button["email"] = 1
            return True

        else:
            self.email_error_message.set("Invalid Email Format")
            button["email"] = 0
            return False

    def Validate_Password(self, event):

        if event.postchangetext == "":
            self.password_error_message.set("")
            button["password"] = 0
            return True

        elif len(event.postchangetext) < 8:
            self.password_error_message.set("Password must contain at least 8 characters")
            button["password"] = 0
            return False

        elif re.search("[^a-zA-Z0-9_]", event.postchangetext) is not None:
            self.password_error_message.set("Password may only contain alphanumeric characters")
            button["password"] = 0
            return False

        elif re.search("[a-zA-Z]+", event.postchangetext) is None:
            self.password_error_message.set("Password must contain an alphabet")
            button["password"] = 0
            return False

        elif re.search("[0-9]+", event.postchangetext) is None:
            self.password_error_message.set("Password must contain a number")
            button["password"] = 0
            return False

        else:
            self.password_error_message.set("")
            button["password"] = 1
            return True

    def Validate_Username_Email(self, event):

        if event.postchangetext == "":
            self.password_error_message.set("")
            button["username_email"] = 0
            return True

        else:
            button["username_email"] = 1
            return True



populate = {"username": "Ruby Rose",
            "email": 'RWBY@protonmail.com',
            "password": "WeissSchnee39"}

button = {"username": 0,
          "email": 0,
          "password": 0,
          "username_email": 0}

# Destroys Register Window and Creates Login Window
def Start_Login(root, window, Credentials, Visuals):
    Credentials.username.set("")
    Credentials.email.set("")
    Credentials.password.set("")
    window.destroy()
    Login(root, Credentials, Visuals)

# Destroys Login Window and Creates Register Window
def Start_Register(root, window, Credentials, Visuals):
    Credentials.username.set("")
    Credentials.email.set("")
    Credentials.password.set("")
    window.destroy()
    Registration(root, Credentials, Visuals)

def Sign_Up(root, window, Credentials, Visuals, Button):
    if Database.RegisterUser(Credentials) is True:
        dialogs.Messagebox.ok(title="Success!", message="User successfully registered!", parent=window)
        Start_Login(root, window, Credentials, Visuals)
    else:
        Credentials.username.set("")
        Button.configure(state="disabled")

def Log_In(root, window, Credentials, Visuals):
    if Database.LoginUser(Credentials) is True:
        print("success")
        noti = dialogs.Messagebox.ok("Successfully logged in!", "Success", parent=window)
        #window.wait_window(noti)


        # Start Dashboard
        MainPage = Dashboard.Dashboard(root, Visuals, Credentials)
        MainPage.Create_Expense()

        window.destroy()

    else:
        dialogs.Messagebox.ok(title=":(", message="Invalid Login Credentials")

# Deletes the preview text when user focuses an Entry Widget
def Delete_Text(event, Visuals):
    if str(event.widget.cget("foreground")) == str(Visuals.colors.get("secondary")):
        event.widget.delete(0, "end")
        event.widget.configure(foreground="black")

# Populates the preview text when user un-focuses an empty Entry widget
def Populate_Text(self, text, key, Visuals):
    if text.get() == "":
        self.widget.insert(0, populate[key])
        self.widget.configure(foreground=Visuals.colors.get("secondary"))


# Checks if button should be enabled
def ButtonCheck(Event, Button):

    if button["username"] + button["password"] + button["email"] == 3:
        Button.configure(state="enabled")

    else:
        Button.configure(state="disabled")

def ButtonCheck2(Event, Button):

    if button["username_email"] + button["password"] == 2:
        Button.configure(state="enabled")

    else:
        Button.configure(state="disabled")


def Registration(root, Credentials, Visuals):

    # Creates Top Level Window
    TopLevel = tkinter.Toplevel(root)
    TopLevel.title("Register Page")
    TopLevel.columnconfigure(0, weight=1)
    TopLevel.rowconfigure(0, weight=1)


    # Creates Main Frame
    mainframe = ttk.Label(TopLevel)
    mainframe.grid(column=0, row=0, sticky="nwes")
    mainframe.columnconfigure(0, weight=1)
    mainframe.columnconfigure(1, weight=1, minsize=400)
    mainframe.rowconfigure(0, weight=1)


    # Creates Left Frame
    lFrame = ttk.Label(mainframe)
    lFrame.grid(column=0, row=0, sticky="nwes")

    # Creates Right Frame
    rFrame = ttk.Label(mainframe)
    rFrame.grid(column=1, row=0, sticky="nwes")


    # Creates Left Frame Widgets
    # Image
    ttk.Label(lFrame, anchor="center", image=Credentials.image).grid(column=1, row=3, sticky="nwes")

    # Welcome Label
    ttk.Label(lFrame, text="Welcome To ExpenseMate!", font=Visuals.Header, foreground="Black",
              anchor="center").grid(column=1, row=2, sticky="swe")

    # Text
    text = tkinter.Text(lFrame, autostyle=0, bg="white",bd=0, highlightthickness=0, height=4, wrap="word", font=Visuals.Text, fg="black")
    text.configure(highlightbackground="white")
    text.tag_configure('tag-center', justify='center')
    text.insert("1.0", "We have freshly baked cookies for new visitors! ;>", "tag-center")
    text["state"] = "disabled"
    text.grid(column=1, row=4, sticky="nwe")

    # Left Frame Resizing
    lFrame.columnconfigure(1, weight=1)
    lFrame.rowconfigure(1, weight=1)
    lFrame.rowconfigure(2, weight=1)
    lFrame.rowconfigure(3, weight=1)
    lFrame.rowconfigure(4, weight=1)
    lFrame.rowconfigure(5, weight=1)


    # Create Right Widgets
    # Get Started (Label)
    ttk.Label(rFrame, text="Get Started", font=Visuals.Header, foreground="black", anchor="center").grid(
        column=1, row=2, sticky="we")

    # Already Have an account? Sign In! (Frame/Label/Button)
    SmallFrame = ttk.Frame(rFrame)
    SmallFrame.grid(column=1, row=3, sticky="nwes")
    SmallFrame.columnconfigure(1, weight=1)
    SmallFrame.columnconfigure(2, weight=1)
    SmallFrame.rowconfigure(3, weight=1)

    ttk.Label(SmallFrame, text="Already have an account?", font=Visuals.Text, anchor="e").grid(column=1, row=3, sticky="nes")
    ttk.Button(SmallFrame, text="Sign In", bootstyle="info-link", command=lambda: Start_Login(root, TopLevel, Credentials, Visuals)).grid(column=2, row=3, sticky="nws")

    # Username (Frame)
    Username_Frame = ttk.Frame(rFrame)
    Username_Frame.grid(column=1, row=4, sticky="nwes", padx=50)
    Username_Frame.columnconfigure(1, weight=1)
    Username_Frame.rowconfigure(1, weight=1)
    Username_Frame.rowconfigure(2, weight=0)
    Username_Frame.rowconfigure(3, weight=1)

    # Username (Label)
    ttk.Label(Username_Frame, text="Username", font=Visuals.Text).grid(column=1, row=1, sticky="swe")

    # Username Box (Entry)
    u = ttk.Entry(Username_Frame, textvariable=Credentials.username, font=Visuals.Text,
                  foreground=Visuals.Theme.colors.get("secondary"), bootstyle="success")
    validate.add_validation(u, validate.validator(Credentials.Validate_Username))
    u.insert(0, "Ruby Rose")
    u.grid(column=1, row=2, sticky="nwe")
    u.bind("<FocusIn>", lambda event, x=Visuals.Theme: Delete_Text(event, x))
    u.bind("<FocusOut>",
           lambda event, x=Credentials.username, y="username", z=Visuals.Theme: Populate_Text(event, x, y, z))
    u.bind("<Return>", lambda event: e.focus())

    # Username Error Message (Label)
    ttk.Label(Username_Frame, textvariable=Credentials.username_error_message, font=Visuals.Error_Text,
              foreground=Visuals.Theme.colors.get("danger")).grid(column=1, row=3, sticky="nwe")


    # Email (Frame)
    Email_Frame = ttk.Frame(rFrame)
    Email_Frame.grid(column=1, row=5, sticky="nwes", padx=50)
    Email_Frame.columnconfigure(1, weight=1)
    Email_Frame.rowconfigure(1, weight=0)
    Email_Frame.rowconfigure(2, weight=0)
    Email_Frame.rowconfigure(3, weight=0)

    # Email (Label)
    ttk.Label(Email_Frame, text="Email", font=Visuals.Text).grid(column=1, row=1, sticky="swe")

    # Email Box (Entry)
    e = ttk.Entry(Email_Frame, textvariable=Credentials.email, font=Visuals.Text,
                  foreground=Visuals.Theme.colors.get("secondary"), bootstyle="success")
    validate.add_validation(e, validate.validator(Credentials.Validate_Email))
    e.insert(0, 'RWBY@protonmail.com')
    e.grid(column=1, row=2, sticky="nwe")
    e.bind("<FocusIn>", lambda event, x=Visuals.Theme: Delete_Text(event, x))
    e.bind("<FocusOut>",
           lambda event, x=Credentials.email, y="email", z=Visuals.Theme: Populate_Text(event, x, y, z))
    e.bind("<Return>", lambda event: p.focus())

    # Email Error Message (Label)
    ttk.Label(Email_Frame, textvariable=Credentials.email_error_message, font=Visuals.Error_Text,
              foreground=Visuals.Theme.colors.get("danger")).grid(column=1, row=3, sticky="nwe")


    
    # Password (Frame)
    Password_Frame = ttk.Frame(rFrame)
    Password_Frame.grid(column=1, row=6, sticky="nwes", padx=50)
    Password_Frame.columnconfigure(1, weight=1)
    Password_Frame.rowconfigure(1, weight=1)
    Password_Frame.rowconfigure(2, weight=0)
    Password_Frame.rowconfigure(3, weight=1)

    # Password (Label)
    ttk.Label(Password_Frame, text="Password", font=Visuals.Text).grid(column=1, row=1, sticky="swe")

    # Password Box (Entry)
    p = ttk.Entry(Password_Frame, textvariable=Credentials.password, font=Visuals.Text, show="*", bootstyle="success",
                  foreground=Visuals.Theme.colors.get(
                      "secondary"))
    validate.add_validation(p, validate.validator(Credentials.Validate_Password))
    p.grid(column=1, row=2, sticky="nwe")
    p.insert(0, "WeissSchnee39")
    p.bind("<FocusIn>", lambda event, z=Visuals.Theme: Delete_Text(event, z))
    p.bind("<FocusOut>",
           lambda event, x=Credentials.password, y="password", z=Visuals.Theme: Populate_Text(event, x, y, z))

    # Password Error Message (Label)
    ttk.Label(Password_Frame, textvariable=Credentials.password_error_message, font=Visuals.Error_Text,
              foreground=Visuals.Theme.colors.get("danger")).grid(column=1, row=3, sticky="nwe")

    # Privacy Policy
    ttk.Checkbutton(rFrame, text="I agree to the terms and conditions", bootstyle="light").grid(column=1, row=7, sticky="we", padx=50)

    # Sign Up Button
    Button = ttk.Button(rFrame, text="Sign Up", bootstyle="success", command=lambda: Sign_Up(root, TopLevel, Credentials, Visuals, Button), state="disabled")
    Button.grid(column=1, row=8, sticky="we", padx=100)
    TopLevel.bind("<FocusOut>", lambda event, x=Button: ButtonCheck(event, x))



    # Right Frame Resizing
    rFrame.columnconfigure(1, weight=1)
    rFrame.rowconfigure(1, weight=2)
    rFrame.rowconfigure(2, weight=1)
    rFrame.rowconfigure(3, weight=0)
    rFrame.rowconfigure(4, weight=1)
    rFrame.rowconfigure(5, weight=0)
    rFrame.rowconfigure(6, weight=1)
    rFrame.rowconfigure(7, weight=0)
    rFrame.rowconfigure(8, weight=1)
    rFrame.rowconfigure(9, weight=1)
    rFrame.rowconfigure(15, weight=3)



def Login(root, Credentials, Visuals):
    # Creates Top Level Window
    TopLevel = tkinter.Toplevel(root)
    TopLevel.title("Login Page")
    TopLevel.columnconfigure(0, weight=1)
    TopLevel.rowconfigure(0, weight=1)

    # Creates Main Frame
    mainframe = ttk.Label(TopLevel)
    mainframe.grid(column=0, row=0, sticky="nwes")
    mainframe.columnconfigure(0, weight=1)
    mainframe.columnconfigure(1, weight=1, minsize=400)
    mainframe.rowconfigure(0, weight=1)

    # Creates Left Frame
    lFrame = ttk.Label(mainframe)
    lFrame.grid(column=0, row=0, sticky="nwes")

    # Creates Right Frame
    rFrame = ttk.Label(mainframe)
    rFrame.grid(column=1, row=0, sticky="nwes")

    # Creates Left Frame Widgets
    # Image
    ttk.Label(lFrame, anchor="center", image=Credentials.image).grid(column=1, row=3, sticky="nwes")

    # Welcome Label
    ttk.Label(lFrame, text="Welcome To ExpenseMate!", font=Visuals.Header, foreground="Black",
              anchor="center").grid(column=1, row=2, sticky="swe")

    # Text
    text = tkinter.Text(lFrame, autostyle=0, bg="white", highlightthickness=0, height=4, wrap="word", font=Visuals.Text,
                        fg="black", bd=0)
    text.tag_configure('tag-center', justify='center')
    text.insert("1.0", "Gimme a break. Christ on a pogo stick, somebody just shoot me, please!", "tag-center")
    text["state"] = "disabled"
    text.grid(column=1, row=4, sticky="nwe")

    # Left Frame Resizing
    lFrame.columnconfigure(1, weight=1)
    lFrame.rowconfigure(1, weight=1)
    lFrame.rowconfigure(2, weight=1)
    lFrame.rowconfigure(3, weight=1)
    lFrame.rowconfigure(4, weight=1)
    lFrame.rowconfigure(5, weight=1)

    # Create Right Widgets
    # Sign In (Label)
    ttk.Label(rFrame, text="Sign In", font=Visuals.Header, foreground="black", anchor="center").grid(
        column=1, row=2, sticky="we")

    # Already Have an account? Sign In! (Frame/Label/Button)
    SmallFrame = ttk.Frame(rFrame)
    SmallFrame.grid(column=1, row=3, sticky="nwes")
    SmallFrame.columnconfigure(1, weight=1)
    SmallFrame.columnconfigure(2, weight=1)
    SmallFrame.rowconfigure(3, weight=1)

    ttk.Label(SmallFrame, text="First time around here?", font=Visuals.Text, anchor="e").grid(
        column=1, row=3,
        sticky="nes")
    ttk.Button(SmallFrame, text="Sign Up", bootstyle="info-link", command=lambda: Start_Register(root, TopLevel, Credentials, Visuals)).grid(column=2, row=3, sticky="nws")  # command=lambda: self.Start_Login(u, e, p, TopLevel)

    # Username/Email (Frame)
    Username_Frame = ttk.Frame(rFrame)
    Username_Frame.grid(column=1, row=4, sticky="nwes", padx=50)
    Username_Frame.columnconfigure(1, weight=1)
    Username_Frame.rowconfigure(1, weight=1)
    Username_Frame.rowconfigure(2, weight=0)
    Username_Frame.rowconfigure(3, weight=1)

    # Username/Email (Label)
    ttk.Label(Username_Frame, text="Username/Email", font=Visuals.Text).grid(column=1, row=1, sticky="swe")

    # Username Box (Entry)
    u = ttk.Entry(Username_Frame, textvariable=Credentials.username, font=Visuals.Text,
                  foreground=Visuals.Theme.colors.get("secondary"), bootstyle="success")
    validate.add_validation(u, validate.validator(Credentials.Validate_Username_Email))
    u.insert(0, "Ruby Rose")
    u.grid(column=1, row=2, sticky="nwe")
    u.bind("<FocusIn>", lambda event, x=Visuals.Theme: Delete_Text(event, x))
    u.bind("<FocusOut>",
           lambda event, x=Credentials.username, y="username", z=Visuals.Theme: Populate_Text(event, x, y, z))
    u.bind("<Return>", lambda event: p.focus())

    # Username Error Message (Label)
    ttk.Label(Username_Frame, textvariable=Credentials.username_error_message, font=Visuals.Error_Text,
              foreground=Visuals.Theme.colors.get("danger")).grid(column=1, row=3, sticky="nwe")

    # Password (Frame)
    Password_Frame = ttk.Frame(rFrame)
    Password_Frame.grid(column=1, row=5, sticky="nwes", padx=50)
    Password_Frame.columnconfigure(1, weight=1)
    Password_Frame.rowconfigure(1, weight=1)
    Password_Frame.rowconfigure(2, weight=0)
    Password_Frame.rowconfigure(3, weight=1)

    # Password (Label)
    ttk.Label(Password_Frame, text="Password", font=Visuals.Text).grid(column=1, row=1, sticky="swe")

    # Password Box (Entry)
    p = ttk.Entry(Password_Frame, textvariable=Credentials.password, font=Visuals.Text, show="*", bootstyle="success",
                  foreground=Visuals.Theme.colors.get(
                      "secondary"))
    validate.add_validation(p, validate.validator(Credentials.Validate_Password))
    p.grid(column=1, row=2, sticky="nwe")
    p.insert(0, "WeissSchnee39")
    p.bind("<FocusIn>", lambda event, z=Visuals.Theme: Delete_Text(event, z))
    p.bind("<FocusOut>",
           lambda event, x=Credentials.password, y="password", z=Visuals.Theme: Populate_Text(event, x, y, z))

    # Password Error Message (Label)
    ttk.Label(Password_Frame, textvariable=Credentials.password_error_message, font=Visuals.Error_Text,
              foreground=Visuals.Theme.colors.get("danger")).grid(column=1, row=3, sticky="nwe")

    # Sign Up Button
    Button = ttk.Button(rFrame, text="Sign In", bootstyle="success", command= lambda :Log_In(root, TopLevel, Credentials, Visuals), state="disabled")
    Button.grid(column=1, row=6, sticky="we", padx=100)
    TopLevel.bind("<FocusOut>", lambda event, x=Button: ButtonCheck2(event, x))

    # Right Frame Resizing
    rFrame.columnconfigure(1, weight=1)
    rFrame.rowconfigure(1, weight=3)
    rFrame.rowconfigure(2, weight=0)
    rFrame.rowconfigure(3, weight=2)
    rFrame.rowconfigure(4, weight=0)
    rFrame.rowconfigure(5, weight=2)
    rFrame.rowconfigure(6, weight=1)
    rFrame.rowconfigure(7, weight=1)
    rFrame.rowconfigure(8, weight=1)
    rFrame.rowconfigure(9, weight=1)
    rFrame.rowconfigure(15, weight=2)



if __name__ == "__main__":
    pass




