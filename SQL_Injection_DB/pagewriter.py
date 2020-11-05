"""
Filename: pagewriter.py
Author(s): Rayan Hamza
Purpose: write html pages unique to users in the templates folder so that they may be used in app.py,
         and so that they may display appropriate information.
"""
import pyodbc

# connect to the database using pyodbc
conn = pyodbc.connect('Driver={SQL Server};' # I am using SQL Server Express
                      'Server=DESKTOP-G1UAJBM\SQLEXPRESS;' # Connecting on my home device
                      'Database=4471_Project;' # This is the name of the database I created
                      'Trusted_Connection=yes;')

# establish a cursor to execute queries
cursor = conn.cursor()

# the header for the user table
user_header = ["id","ssn","first_name","last_name","username",'password',"email","gender",'ip_address','creditcard_no','address',
               "state","city","zip_code"]

emp_header = ["Employee ID","First name","Last name", "username","position","salary","department number","department name",
              "supervisor"]

prod_header = []

depart_header = []


def writeuser(username, password):
    cursor.execute('SELECT * FROM Users WHERE username=\'' + username +
                   '\' and [password] = \''+password+'\';')
    if len(list(cursor)) > 0:
        # start writing the file
        file = open('templates/user.html','w+')
        file.write('<!DOCTYPE html>\n<html>\n')
        cursor.execute('SELECT * FROM Users WHERE username=\'' + username +
                       '\' and [password] = \'' + password + '\';')
        name = list(cursor)[0][2]
        file.write('<head>\n<title>'+name + '\'s page'+'</title>\n')
        file.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        file.write('<link href="static/bootstrap-reboot.css" rel="stylesheet" media="screen">\n</head>')
        file.write('<body>\n')
        file.write('<h1> Welcome '+ name+'</h1>\n<br>\n')
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
        return 0
    return "error"

def writeemp(username, password):
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
        file.write('<head>\n<title>' + name + '\'s Portal' + '</title>\n')
        file.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        file.write('<link href="static/bootstrap-reboot.css" rel="stylesheet" media="screen">\n</head>')
        file.write('<body>\n')
        file.write('<h1> Welcome ' + name + '</h1>\n<br>\n')
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
        return 0
    return "error"

def writeprod(product):
    cursor.execute('SELECT * FROM Products WHERE productID=\'' + product +'\';')
    if len(list(cursor)) > 0:
        # start writing the file
        file = open('templates/products.html','w+')
        file.write('<!DOCTYPE html>\n<html>\n')
        cursor.execute('SELECT * FROM Products WHERE productID=\'' + product +'\';')
        name = list(cursor)[0][2]
        file.write('<head>\n<title>'+name + '\'s page'+'</title>\n')
        file.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        file.write('<link href="static/bootstrap-reboot.css" rel="stylesheet" media="screen">\n</head>')
        file.write('<body>\n')
        file.write('<h1> Welcome '+ name+'</h1>\n<br>\n')
        file.write('<p>Click <a href="logout">here</a> to go log out.</p>\n')
        file.write('<p>')
        file.write('<table style=\"width:100%\">\n')
        # write the table header
        file.write('<tr>\n')
        for heading in prod_header:
            file.write('\t<th>'+heading+'</th>\n')
        file.write('</tr>\n')
        cursor.execute('SELECT * FROM Products WHERE productID=\'' + product +'\';')
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
    cursor.execute('SELECT * FROM Department WHERE Name=\'' + department + '\';')
    if len(list(cursor)) > 0:
        # start writing the file
        file = open('templates/department.html','w+')
        file.write('<!DOCTYPE html>\n<html>\n')
        cursor.execute('SELECT * FROM Department WHERE Name=\'' + department + '\';')
        name = list(cursor)[0][2]
        file.write('<head>\n<title>'+name + '\'s page'+'</title>\n')
        file.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        file.write('<link href="static/bootstrap-reboot.css" rel="stylesheet" media="screen">\n</head>')
        file.write('<body>\n')
        file.write('<h1> Welcome '+ name+'</h1>\n<br>\n')
        file.write('<p>Click <a href="logout">here</a> to go log out.</p>\n')
        file.write('<p>')
        file.write('<table style=\"width:100%\">\n')
        # write the table header
        file.write('<tr>\n')
        for heading in depart_header:
            file.write('\t<th>'+heading+'</th>\n')
        file.write('</tr>\n')
        cursor.execute('SELECT * FROM Department WHERE Name=\'' + department + '\';')
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
