"""
Filename: app.py
Author(s): Rayan Hamza, Abhishek Salandri
Purpose: create the application that the user can interact with

*This code is inspired by the Discover Flask series on the realpython website.
- the tutorials are hosted by Michael Herman, and are as of 2014
"""

import pagewriter as pw
from flask import Flask, render_template, redirect, url_for, request, session, flash

# create the application
app = Flask(__name__)

app.secret_key = "I am cool" # set a key for user authentication

# the home page, so to speak
@app.route('/')
def home():
    return render_template("welcome.html")

# Route for handling the general login page logic
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

# Route for handling the employee login page logic
@app.route('/emplogin', methods=['GET', 'POST'])
def emplogin():
    error = None
    if request.method == 'POST':
        erflag = pw.writeemp(request.form['username'], request.form['password'])
        if erflag == "error":
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            # flash('You were just logged in!')
            return redirect(url_for('employeeportal'))
    return render_template('employeelogin.html', error=error)

# Route for handling the product page logic
@app.route('/products', methods=['GET', 'POST'])
def products():
    error = None
    if request.method == 'POST':
        erflag = pw.writeprod(request.form['product'])
        if erflag == "error":
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            # flash('You were just logged in!')
            return redirect(url_for('product'))
    return render_template('productsSearch.html', error=error)

# Route for handling the department page logic
@app.route('/departments', methods=['GET', 'POST'])
def departments():
    error = None
    if request.method == 'POST':
        erflag = pw.writedepart(request.form['department'])
        if erflag == "error":
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            # flash('You were just logged in!')
            return redirect(url_for('department'))
    return render_template('departmentsSearch.html', error=error)

# finish the user's session
@app.route('/logout')
def logout():
    pw.clearuser()
    session.pop('logged_in',None)
    flash('You were just logged out!')
    return redirect(url_for('home'))

# The user's personal page
@app.route('/user')
def user():
    return render_template("user.html")

# The employee's portal page
@app.route('/employeeportal')
def employeeportal():
    return render_template("employeeportal.html")

@app.route('/product')
def product():
    return render_template("products.html")

@app.route('/department')
def department():
    return render_template("departments.html")

@app.route('/transaction')
def transaction():
    pw.writetrans()
    return render_template("transactions.html")

@app.route('/supplier')
def supplier():
    pw.writesup()
    return render_template("suppliers.html")

@app.route('/store', methods=['GET', 'POST'])
def store():
    pw.writestorepage()
    error = None
    if request.method == 'POST':
        erflag = pw.addtransaction(request.form['ProductID'], request.form['Amount'])
        if erflag == "error2":
            error = 'Amount must be at least $500.00'
        if erflag == "error3":
            error = "ProductID not valid"
        else:
            # flash('You were just logged in!')
            return redirect(url_for('transaction'))
    return render_template('store.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)