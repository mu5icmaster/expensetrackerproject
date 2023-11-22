import tkinter
import ttkbootstrap as ttk
import Login_Page
import Theme

# Creates root window
root = tkinter.Tk()
root.withdraw()

# Sets Theme/Fonts
Visuals = Theme.Visuals(style="flatly")

# Program Start
Credentials = Login_Page.Credentials()
Login_Page.Login(root, Credentials, Visuals)


root.mainloop()