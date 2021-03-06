"""
Filename: app.py
Author(s): Rayan Hamza
Purpose: create the application that the user can interact with

*This code is inspired by the Discover Flask series on the realpython website.
- the tutorials are hosted by Michael Herman, and are as of 2014
"""

import pyodbc
import pagewriter as pw
from flask import Flask, render_template, redirect, url_for, request, session, flash


# connect to the database using pyodbc
conn = pyodbc.connect('Driver={SQL Server};' # I am using SQL Server Express
                      'Server=RAYAN-PC\SQLEXPRESS;' # Connecting on my home device
                      'Database=CompanyABC;' # This is the name of the database I created
                      'Trusted_Connection=yes;')

# establish a cursor to execute queries
cursor = conn.cursor()

# create the application
app = Flask(__name__)

app.secret_key = "I am cool" # set a key for user authentication

# the home page, so to speak
@app.route('/')
def home():
    return render_template("welcome.html")

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        erflag = pw.writeuser(request.form['username'], request.form['password'])
        if erflag == "error":
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            # flash('You were just logged in!')
            return redirect(url_for('user'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('You were just logged out!')
    return redirect(url_for('home'))

@app.route('/user')
def user():
    return render_template("user.html")

if __name__ == '__main__':
    app.run(debug=True)