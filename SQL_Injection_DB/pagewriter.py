"""
Filename: pagewriter.py
Author(s): Rayan Hamza
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

# the header for the user table
user_header = ["id","ssn","first_name","last_name","username",'password',"email","gender",'ip_address','creditcard_no','address',
               "state","city","zip_code"]


def writeuser(username, password):
    cursor.execute('SELECT username FROM Users WHERE username=\'' + username + '\';')
    if username in list(list(cursor)[0]):
        cursor.execute('SELECT [password] FROM Users WHERE username=\'' + username + '\';')
        if password in list(list(cursor)[0]):
            # start writing the file
            file = open('templates/user.html','w+')
            file.write('<!DOCTYPE html>\n<html>\n')
            cursor.execute('SELECT first_name FROM Users WHERE username=\'' + username + '\';')
            name = list(cursor)[0][0]
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

            cursor.execute('SELECT * FROM Users WHERE username=\''+username+
                   '\' and [password] = \''+password+'\';')
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


