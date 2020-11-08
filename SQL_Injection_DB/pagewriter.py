"""
Filename: pagewriter.py
Author(s): Rayan Hamza, Abhishek Salandri
Purpose: write html pages unique to users in the templates folder so that they may be used in app.py,
         and so that they may display appropriate information.
"""
import pyodbc

# connect to the database using pyodbc
conn = pyodbc.connect('Driver={SQL Server};' # I am using SQL Server Express
                      'Server=RAYAN-PC\SQLEXPRESS;' # Connecting on my home device
                      'Database=CompanyABC;' # This is the name of the database I created
                      'Trusted_Connection=yes;')

# establish a cursor to execute queries
cursor = conn.cursor()

# create table headers
user_header = ["id","ssn","first_name","last_name","username",'password',"email","gender",'ip_address','creditcard_no','address',
               "state","city","zip_code"]

emp_header = ["Employee ID","First name","Last name", "username","position","salary","department number","department name",
              "supervisor"]

prod_header = ["ID", "Product ID", "Category", "Supplier ID"]

depart_header = ["Department Number", "Name", "Supervisor Name"]

trans_header = ["transaction_ID","Transaction No.","Credit Card No.","Amount","ProductID","Product"]

#this is how we will track client information
currentuser = None

# this will help verify that the user works
uservalid = False

# method to clear username so info cannot be accessed after logout
def clearuser():
    global  currentuser
    currentuser = None
    return

# TODO: Methods to combat sql injection


def writeuser(username, password):
    """
    Displays the general portal for the user
    :param username: the user's username
    :param password: the user's password
    :return:
    """
    global currentuser, uservalid
    cursor.execute('SELECT * FROM Users WHERE username=\'' + username +
                   '\' and [password] = \''+password+'\';')
    if len(list(cursor)) > 0:
        # start writing the file
        file = open('templates/user.html','w+')
        file.write('<!DOCTYPE html>\n<html>\n')
        cursor.execute('SELECT * FROM Users WHERE username=\'' + username +
                       '\' and [password] = \'' + password + '\';')
        resultset = list(cursor)
        name = resultset[0][2]
        currentuser = resultset[0][4]
        file.write('<head>\n<title>'+name + '\'s page'+'</title>\n')
        file.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        file.write('<link href="static/bootstrap-reboot.css" rel="stylesheet" media="screen">\n</head>')
        file.write('<body>\n')
        file.write('<h1> Welcome '+ name+'</h1>\n<br>\n')
        file.write('<p><a href="transaction">view transactions</a></p>\n')
        file.write('<p>Click <a href="logout">here</a> to go log out.</p>\n')
        file.write('<p>')
        file.write('<table style=\"width:100%\">\n')
        # write the table header
        file.write('<tr>\n')
        for heading in user_header:
            file.write('\t<th>'+heading+'</th>\n')
        file.write('</tr>\n')
        cursor.execute('SELECT * FROM Users WHERE username=\'' + username +
                       '\' and [password] = \'' + password + '\';')
        for row in cursor:
            file.write('<tr>\n')
            for item in row:
                file.write('<td>'+str(item)+'</td>\n')
            file.write('</tr>\n')
        file.write('</table>\n')
        file.write('</p>\n')
        file.write('</body>\n')
        file.write('</html>\n')
        uservalid = True
        return 0
    return "error"

def writeemp(username, password):
    """
    Displays the employee portal page for the employee user
    :param username: the employees username
    :param password: the employees password
    :return:
    """
    global currentuser, uservalid
    part1 = 'd.departmentNo,d.[Name],supervisor_name FROM Employees e join Users u '
    part2 = 'on e.ssn = u.ssn join Department d on e.departmentNo = d.departmentNo '
    part3 = 'WHERE username=\''  + username +'\' and [password] = \'' + password + '\';'
    part0 = 'select e.id,first_name,last_name,username,position,salary,'
    empqry = part0 + part1 + part2 + part3
    cursor.execute(empqry)
    if len(list(cursor)) > 0:
        # start writing the file
        file = open('templates/employeeportal.html', 'w+')
        file.write('<!DOCTYPE html>\n<html>\n')
        cursor.execute(empqry)
        name = list(cursor)[0][1] # should be first name
        currentuser = list(cursor)[0][3]
        file.write('<head>\n<title>' + name + '\'s Portal' + '</title>\n')
        file.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        file.write('<link href="static/bootstrap-reboot.css" rel="stylesheet" media="screen">\n</head>')
        file.write('<body>\n')
        file.write('<h1> Welcome ' + name + '</h1>\n<br>\n')
        #TODO: give an option for employees to go to an additional page

        # file.write('<p><a href="transaction">view transactions</a></p>\n')
        file.write('<p>Click <a href="logout">here</a> to go log out.</p>\n')
        file.write('<p>')
        file.write('<table style=\"width:100%\">\n')
        # write the table header
        file.write('<tr>\n')
        for heading in emp_header:
            file.write('\t<th>' + heading + '</th>\n')
        file.write('</tr>\n')
        cursor.execute(empqry)
        for row in cursor:
            file.write('<tr>\n')
            for item in row:
                file.write('<td>' + str(item) + '</td>\n')
            file.write('</tr>\n')
        file.write('</table>\n')
        file.write('</p>\n')
        file.write('</body>\n')
        file.write('</html>\n')
        uservalid = True
        return 0
    return "error"

def writeprod(product):
    """
    Displays information for the selected product
    :param product: the product ID
    :return: error if erronious or 0
    """
    cursor.execute('SELECT * FROM Products WHERE productID=' + product +';')
    if len(list(cursor)) > 0:
        # start writing the file
        file = open('templates/products.html','w+')
        file.write('<!DOCTYPE html>\n<html>\n')
        cursor.execute('SELECT * FROM Products WHERE productID=' + product +';')
        name = list(cursor)[0][2]
        file.write('<head>\n<title>'+name+ '\'s page'+'</title>\n')
        file.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        file.write('<link href="static/bootstrap-reboot.css" rel="stylesheet" media="screen">\n</head>')
        file.write('<body>\n')
        file.write('<h1> Product: '+ name+'</h1>\n<br>\n')
        file.write('<p>Click <a href="logout">here</a> to return to home page.</p>\n')
        file.write('<p>')
        file.write('<table style=\"width:100%\">\n')
        # write the table header
        file.write('<tr>\n')
        for heading in prod_header:
            file.write('\t<th>'+heading+'</th>\n')
        file.write('</tr>\n')
        cursor.execute('SELECT * FROM Products WHERE productID=' + product +';')
        for row in cursor:
            file.write('<tr>\n')
            for item in row:
                file.write('<td>'+str(item)+'</td>\n')
            file.write('</tr>\n')
        file.write('</table>\n')
        file.write('</p>\n')
        file.write('</body>\n')
        file.write('</html>\n')
        return 0
    return "error"

def writedepart(department):
    """
    Lists the information of the selected department
    :param department: the department name
    :return: error for errors or 0
    """
    cursor.execute('SELECT departmentNo,Name,supervisor_name FROM Department WHERE Name=\'' + department + '\';')
    if len(list(cursor)) > 0:
        # start writing the file
        file = open('templates/departments.html','w+')
        file.write('<!DOCTYPE html>\n<html>\n')
        cursor.execute('SELECT departmentNo,Name,supervisor_name FROM Department WHERE Name=\'' + department + '\';')
        name = list(cursor)[0][1]
        file.write('<head>\n<title>'+ name + '\'s page'+'</title>\n')
        file.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        file.write('<link href="static/bootstrap-reboot.css" rel="stylesheet" media="screen">\n</head>')
        file.write('<body>\n')
        file.write('<h1> Department: '+ name+'</h1>\n<br>\n')
        file.write('<p>Click <a href="logout">here</a> to return to home page.</p>\n')
        file.write('<p>')
        file.write('<table style=\"width:100%\">\n')
        # write the table header
        file.write('<tr>\n')
        for heading in depart_header:
            file.write('\t<th>'+heading+'</th>\n')
        file.write('</tr>\n')
        cursor.execute('SELECT departmentNo,Name,supervisor_name FROM Department WHERE Name=\'' + department + '\';')
        
        for row in cursor:
            file.write('<tr>\n')
            for item in row:
                file.write('<td>'+str(item)+'</td>\n')
            file.write('</tr>\n')
        file.write('</table>\n')
        file.write('</p>\n')
        file.write('</body>\n')
        return 0
    return "error"

def writetrans():
    """
    Writes the transactions page dependent on the username of the current user.
    :return: error for errors or 0
    """
    global currentuser
    transqry = ("SELECT t.*, p.category from Transactions t join Users u on u.creditcard_no = t.creditCardNo "
                "join Products p on t.productID = p.productID "
                "where u.username =\'" + currentuser + "\';")
    cursor.execute(transqry)
    if len(list(cursor)) > 0 or uservalid:
        # start writing the file
        file = open('templates/transactions.html', 'w+')
        file.write('<!DOCTYPE html>\n<html>\n')
        cursor.execute(transqry)
        file.write('<head>\n<title>Transaction History</title>\n')
        file.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        file.write('<link href="static/bootstrap-reboot.css" rel="stylesheet" media="screen">\n</head>')
        file.write('<body>\n')
        file.write('<h1> View your transaction history  </h1>\n<br>\n')
        file.write('<p><a href="user">user page</a></p>\n')
        file.write('<p>Click <a href="logout">here</a> to return to home page.</p>\n')
        file.write('<p>')
        file.write('<table style=\"width:100%\">\n')
        # write the table header
        file.write('<tr>\n')
        for heading in trans_header:
            file.write('\t<th>' + heading + '</th>\n')
        file.write('</tr>\n')
        cursor.execute(transqry)

        for row in cursor:
            file.write('<tr>\n')
            for item in row:
                file.write('<td>' + str(item) + '</td>\n')
            file.write('</tr>\n')
        file.write('</table>\n')
        file.write('</p>\n')
        file.write('</body>\n')
        return 0
    return "error"

#TODO: post additional query pages
