from flask import Flask, request, redirect
from flask import Blueprint,render_template
app = Flask(__name__)
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from datetime import datetime
from flask_cors import CORS, cross_origin
import ibm_db

app = Flask(__name__, template_folder = 'templates')
app.config['SECRET_KEY'] = 'top-secret!'
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = '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'
app.config['MAIL_DEFAULT_SENDER'] = 'rajeshsuriya2019@gmail.com'
mail = Mail(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# GLobal variables
EMAIL=''
USERID=''

#conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=54a2f15b-5c0f-46df-8954-7e38e612c2bd.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32733;Security=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=qwp68812;PWD=gFqcCYZ0DrMzenZ8;","","")

def fetch_walletamount():
    sql = 'SELECT WALLET FROM PETA_USER WHERE EMAIL=?'
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, EMAIL)
    ibm_db.execute(stmt)
    user =ibm_db.fetch_assoc(stmt)
    print(user['WALLET'])
    return user['WALLET'] #returns int
 
def fetch_categories():

    sql = 'SELECT * FROM PETA_CATEGORY WHERE USERID = ?'
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,USERID)
    ibm_db.execute(stmt)

    categories = []
    while ibm_db.fetch_row(stmt) != False:
        categories.append([ibm_db.result(stmt, "CATEGORYID"), ibm_db.result(stmt, "CATEGORY_NAME")])

    sql = 'SELECT * FROM PETA_CATEGORY WHERE USERID IS NULL'
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.execute(stmt)

    while ibm_db.fetch_row(stmt) != False:
        categories.append([ibm_db.result(stmt, "CATEGORYID"), ibm_db.result(stmt, "CATEGORY_NAME")])

    print(categories)
    return categories # returns list 

def fetch_userID():
    sql = 'SELECT USERID FROM PETA_USER WHERE EMAIL=?'
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, EMAIL)
    ibm_db.execute(stmt)
    user=ibm_db.fetch_assoc(stmt)
    print(user['USERID'])
    return user['USERID'] # returns int 

def fetch_groups():
    sql = 'SELECT * FROM PETA_GROUPS'
    stmt = ibm_db.exec_immediate(conn, sql)
    groups = []
    while ibm_db.fetch_row(stmt) != False:
        groups.append([ibm_db.result(stmt, "GROUPID"), ibm_db.result(stmt, "GROUPNAME")])
    print(groups)
    return groups # returns list 

def fetch_expenses() : 
    sql = 'SELECT * FROM PETA_EXPENSE where USERID = ' + str(USERID)
    print(sql)
    stmt = ibm_db.exec_immediate(conn, sql)
    expenses = []
    while ibm_db.fetch_row(stmt) != False:
        category_id = ibm_db.result(stmt, "CATEGORYID")
        category_id = str(category_id)
        sql2 = "SELECT * FROM PETA_CATEGORY WHERE CATEGORYID = " + category_id
        stmt2 = ibm_db.exec_immediate(conn, sql2)
        category_name = ""
        while ibm_db.fetch_row(stmt2) != False :
            category_name = ibm_db.result(stmt2, "CATEGORY_NAME")
        expenses.append([ibm_db.result(stmt, "EXPENSE_AMOUNT"), ibm_db.result(stmt, "DATE"), ibm_db.result(stmt, "DESCRIPTION"), category_name])
    print(expenses)
    return expenses

app.debug = True

@app.route('/')
def landingPage():
    return render_template("landingPage.html")

@app.route('/navbar')
def navbar():
    return render_template("Navbar.html")


@app.route('/contactus')
def contactus():
    return render_template("contactUs.html")

@app.route('/signup')
def signup():
    return render_template("signUp.html")

@app.route('/signin')
def signin():
    return render_template("signIn.html")

@app.route('/aboutus')
def aboutus():
    return render_template("aboutUs.html")

@app.route('/skeleton')
def skeleton():
    return render_template("skeleton.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/addingExpenses')
def addingExpenses():
    return render_template("addingExpenses.html")

@app.route('/categories')
def categories():
    return render_template("categories.html")

@app.route('/reports')
def reports():
    return render_template("addingExpenses.html")

@app.route('/tips')
def tips():
    return render_template("tips.html")

@app.route('/helpnsupport')
def helpnsupport():
    return render_template("helpnsupport.html")
   
    
if __name__ == '__main__':
    app.run()




