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

supp_header = ["ID","Location","Supplier","Supplier ID","Category","ProductID"]

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
        file.write('<table style=\"width:100%\">\n')
        file.write('<tr>\n')
        file.write('<td><p><a href="store">buy a product</a></p></td>\n')
        file.write('<td><p><a href="transaction">view transactions</a></p></td>\n')
        file.write('<td><p>Click <a href="logout">here</a> to go log out.</p></td>\n')
        file.write('</tr>\n')
        file.write('</table>\n')
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
        qrylst = list(cursor).copy()
        name = qrylst[0][1] # should be first name
        currentuser = qrylst[0][3]
        file.write('<head>\n<title>' + name + '\'s Portal' + '</title>\n')
        file.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        file.write('<link href="static/bootstrap-reboot.css" rel="stylesheet" media="screen">\n</head>')
        file.write('<body>\n')
        file.write('<h1> Welcome ' + name + '</h1>\n<br>\n')
        file.write('<table style=\"width:100%\">\n')
        file.write('<tr>\n')
        file.write('<td><p><a href="supplier">view suppliers</a></p></td>\n')
        file.write('<td><p><a href="deleteuser">delete a user</a></p></td>\n')
        file.write('<td><p>Click <a href="logout">here</a> to go log out.</p></td>\n')
        file.write('</tr>\n')
        file.write('</table>\n')
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
    assert not (currentuser == None)
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

def writesup():
    """
        Writes the suppliers page.
        :return: error for errors or 0
        """
    global currentuser
    theqry = ("SELECT s.id,s.location,s.supplier_name,s.supplierID,p.category,p.productID "
               "FROM Supplier s Join Products p ON s.supplierID = p.supplierID;")
    cursor.execute(theqry)
    if len(list(cursor)) > 0 or uservalid:
        # start writing the file
        file = open('templates/suppliers.html', 'w+', encoding="utf-8")
        file.write('<!DOCTYPE html>\n<html>\n')
        cursor.execute(theqry)
        file.write('<head>\n<title>Suppliers</title>\n')
        file.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        file.write('<link href="static/bootstrap-reboot.css" rel="stylesheet" media="screen">\n</head>')
        file.write('<body>\n')
        file.write('<h1> Suppliers of Products  </h1>\n<br>\n')
        file.write('<p><a href="employeeportal">back to portal</a></p>\n')
        file.write('<p>Click <a href="logout">here</a> to return to home page.</p>\n')
        file.write('<p>')
        file.write('<table style=\"width:100%\">\n')
        # write the table header
        file.write('<tr>\n')
        for heading in supp_header:
            file.write('\t<th>' + heading + '</th>\n')
        file.write('</tr>\n')
        cursor.execute(theqry)

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

"""
Dylan's Queries #####################################################
"""

updateuserloc = "UPDATE USERS SET address = '%s', state='%s',city='%s',zipcode='%s' WHERE username=%s;"

updateTrans = "UPDATE Transactions SET amount = $%.2f WHERE id=%d;"

updateuserinfo = "UPDATE Users SET username = '%s', password = '%s' WHERE username = %s;"

updateSalary = "UPDATE Employees SET salary = $%.2f WHERE id = %s;"

deleteUser = "DELETE FROM Users WHERE username = '%s'"

deleteTrans = "DELETE FROM Transactions WHERE id = %d"

"""
These are the functions to execute the queries
"""
def updateloc(address, state, city, zip):
    global currentuser
    query = updateuserloc % (address,state,city,zip,currentuser)
    cursor.execute(query)

def updateTrans(amount, id):
    cursor.execute(updateTrans % (float(amount), int(id)))

def updateusername(newusername, newpass):
    global currentuser
    # first, we must check for uniqueness
    checkqry = "SELECT username FROM Users"
    cursor.execute(checkqry)
    userlist = []
    for row in cursor:
        userlist.append(row[0])
    if newusername in userlist:
        return "error"
    cursor.execute(updateuserinfo % (newusername,newpass,currentuser))
    # update the current user variable as well
    currentuser = newusername

def updatesalary(amount, id):
    cursor.execute(updateSalary % (float(amount), int(id)))
    conn.commit()

def deleteuser(usrnm):
    cursor.execute(deleteUser % (usrnm))
    conn.commit()

def deletetransaction(id):
    cursor.execute(deleteTrans % (id))
    conn.commit()
"""
Back to writing pages #################################################
"""
def addtransaction(product_id, amount):
    """
    Adds the new transaction done by the user
    :param product_id: the product they want to buy
    :param amount: the amount they will spend
    :return:
    """
    global currentuser
    global conn
    assert not (currentuser == None)
    def isfloat(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    query = "INSERT INTO Transactions VALUES(%d,%d,%s,$%.2f,%d);"
    if (not isfloat(amount)) or float(amount) < 500:
        return "error2"
    cursor.execute("SELECT productID from Products;")
    productlist = []
    for row in cursor:
        productlist.append(row[0])
    if float(product_id) not in productlist:
        return "error3"
    cursor.execute("SELECT MAX(id) FROM Transactions;")
    last_id = list(cursor)[0][0]
    cursor.execute("SELECT MAX(transactionNo) FROM Transactions;")
    last_trans = list(cursor)[0][0]
    cursor.execute("SELECT creditcard_no FROM Users WHERE username = \'"+currentuser+"\';")
    creditcard = list(cursor)[0][0]
    # execute the query and commit it to the db
    cursor.execute(query % (int(last_id)+1,int(last_trans)+1,creditcard,float(amount),int(float(product_id))))
    conn.commit()
    return 0


def writestorepage():
    """
        Writes the store page.
        :return: error for errors or 0
        """
    global currentuser
    theqry = "SELECT * FROM Products"
    cursor.execute(theqry)
    resultset = list(cursor)
    if len(resultset) > 0 or uservalid:
        # start writing the file
        file = open('templates/store.html', 'w+', encoding="utf-8")
        file.write('<!DOCTYPE html>\n<html>\n')
        file.write('<head>\n<title>Store</title>\n')
        file.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        file.write('<link href="static/bootstrap-reboot.css" rel="stylesheet" media="screen">\n</head>')
        file.write('<body>\n')
        file.write('<h1> Buy A Product </h1>\n<br>\n')
        file.write('<p>Click <a href="logout">here</a> to return to home page.</p>\n')
        file.write('<form action="" method="post">\n')
        file.write('<input type="text" placeholder="ProductID" name="ProductID" value="{{')
        file.write('request.form.ProductID }}">\n')
        file.write('<input type="text" placeholder="Amount" name="Amount" value="{{')
        file.write('request.form.Amount }}">\n')
        file.write('<input class="btn btn-default" type="submit" value="Purchase">\n')
        file.write('</form>\n')
        file.write('{% if error %}\n')
        file.write('  <p class="error"><strong>Error:</strong> {{ error }}\n')
        file.write('{% endif %}\n')
        file.write('{% for message in get_flashed_messages() %}\n')
        file.write('  {{ message }}\n')
        file.write('{% endfor %}\n')
        file.write('<p>')
        file.write('<table style=\"width:100%\">\n')
        # write the table header
        file.write('<tr>\n')
        for heading in prod_header:
            file.write('\t<th>' + heading + '</th>\n')
        file.write('</tr>\n')
        cursor.execute(theqry)
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

def deletesuccess(usrnm):
    deleteuser(usrnm)
    file = open('templates/deletesuccess.html', 'w+', encoding="utf-8")
    file.write('<!DOCTYPE html>\n')
    file.write('<html>\n')
    file.write('  <head>\n')
    file.write('    <title>Delete Success</title>\n')
    file.write('    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
    file.write('    <link href="static/bootstrap-reboot.css" rel="stylesheet" media="screen">\n')
    file.write('  </head>\n')
    file.write('  <header>\n')
    file.write('    <image src="{{ url_for(\'static\', filename=\'Website Icons.png\')}}"/>\n')
    file.write('  </header>\n')
    file.write('  <body>\n')
    file.write('    <h1>The User ' + usrnm +' was successfully deleted</h1>\n')
    file.write('    <br>\n')
    file.write('<p><a href="employeeportal">back to employee portal</a></p>\n')
    return 0