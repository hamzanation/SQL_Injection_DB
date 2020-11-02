import pyodbc
from tkinter import *
from functools import partial

# connect to the database using pyodbc
conn = pyodbc.connect('Driver={SQL Server};' # I am using SQL Server Express
                      'Server=DESKTOP-G1UAJBM\SQLEXPRESS;' # Connecting on my home device
                      'Database=4471_Project;' # This is the name of the database I created
                      'Trusted_Connection=yes;')

# establish a cursor to execute queries
cursor = conn.cursor()
# the attributes of the user relation
user_header = ["id","ssn","first_name","last_name","username",'password',"email","gender",'ip_address','creditcard_no','address',
               "state","city","zip_code"]
# Create the loginwindow
tkWindow = Tk()
tkWindow.geometry('400x150')
tkWindow.title('Tkinter Login Form - pythonexamples.org')

# The function to transition to the user window
def userWindow(cursor):
    global tkWindow
    tkWindow.destroy() # destroy the login
    tkWindow = Tk()
    tkWindow.title('User Information')
    k = 0
    for header in user_header: # add the header of the table
        Label(text = header).grid(row=0,column = k)
        k = k + 1
    for row in cursor: # add the acual data
        Label(text=row).grid(columnspan=len(user_header))
    return

# The function to go from the login window to the next window
def validateLogin(username, password):
	#print("username entered :", username.get())
	#print("password entered :", password.get())
	cursor.execute('SELECt * FROM Users WHERE username=\''+username.get()+
                   '\' and [password] = \''+password.get()+'\';')
	userWindow(cursor)
	return




#username label and text entry box
Label(tkWindow, text="User Name").grid(row=0, column=0)
username = StringVar()
Entry(tkWindow, textvariable=username).grid(row=0, column=1)

#password label and password entry box
Label(tkWindow,text="Password").grid(row=1, column=0)
password = StringVar()
Entry(tkWindow, textvariable=password, show='*').grid(row=1, column=1)

# check the credentials
validateLogin = partial(validateLogin, username, password)

#login button
Button(tkWindow, text="Login", command=validateLogin).grid(row=4, column=0)

tkWindow.mainloop()
"""
cursor.execute('SELECT * FROM Department')
for row in cursor:
    print(row)
"""