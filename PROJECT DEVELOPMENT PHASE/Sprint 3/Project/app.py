from flask import Flask, session, redirect, render_template, request, url_for
import ibm_db, re

app = Flask(_name_)
app.secret_key = "sss"

connection = ibm_db.connect("DATABASE=bludb;HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30376;SECURITY=SSL;SSLServerCertificate=DigiCert.crt;UID=zbx23177;PWD=0609PXFDuWyfoBlJ",'','')

info = ""


@app.route('/')
def main():
    if session and session['active']:
        return redirect(url_for("expenses"))
    else:
        page = "login"
        if request.values.get('query') == "register":
            page = "register"

        return render_template('index.html', info=info, page=page)


@app.route('/create-account', methods=['POST'])
def create():
    global info
    if request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        pwd = request.form["password"]

        stmt = ibm_db.prepare(connection, "SELECT * FROM account WHERE email=?")
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)

        acc = ibm_db.fetch_assoc(stmt)

        if acc:
            info = "Email Already exists"
            return redirect(url_for('main', query="register"))
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            info = "Enter a valid Email"
            return redirect(url_for('main', query="register"))
        else:
            info = ""

            stmt1 = ibm_db.prepare(connection, "INSERT INTO account VALUES (?,?,?)")
            ibm_db.bind_param(stmt1, 1, name)
            ibm_db.bind_param(stmt1, 2, pwd)
            ibm_db.bind_param(stmt1, 3, email)
            ibm_db.execute(stmt1)

            session['active'] = True
            session['email'] = email

            return redirect(url_for("expenses"))


@app.route('/login', methods=['POST'])
def login():
    global info
    if request.method == "POST":
        email = request.form["email"]
        pwd = request.form["password"]

        stmt = ibm_db.prepare(connection, "SELECT * FROM account WHERE email=? AND password=?")
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.bind_param(stmt, 2, pwd)
        ibm_db.execute(stmt)
        acc = ibm_db.fetch_assoc(stmt)
        print(acc)

        if acc:
            info = ""
            session['active'] = True
            session['email'] = acc['EMAIL']
            return redirect(url_for('expenses'))
        else:
            info = "Email and Password doesn't match"
            return redirect(url_for('main'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main'))


@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    global info
    expenses_amount = [0, 0, 0, 0, 0]
    expenses_list = []

    if session and session['active']:
        email = session['email']
        stmt = ibm_db.prepare(connection, "SELECT expense, date, expense_type, amount FROM expenses WHERE email=?")
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)
        val = ibm_db.fetch_assoc(stmt)
        while val:
            expenses_list.append(val)
            if val['EXPENSE_TYPE'] == "Home":
                amount_index = 0
            elif val['EXPENSE_TYPE'] == "Personal":
                amount_index = 1
            elif val['EXPENSE_TYPE'] == "Entertainment":
                amount_index = 2
            elif val['EXPENSE_TYPE'] == "Health Care":
                amount_index = 3
            else:
                amount_index = 4
            expenses_amount[amount_index] += val['AMOUNT']

            val = ibm_db.fetch_assoc(stmt)

        print(expenses_amount)
        print(expenses_list)

        info = ""
        expenses_list = expenses_list[::-1]

        return render_template("expenses.html", expenses_list=expenses_list, expenses_amount=expenses_amount)
    else:
        info = "Your session is expired"

        return redirect(url_for('main'))


@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        expense_type = request.form["type"]
        date = format_date(request.form["date"])
        expense = request.form["expense"]
        amount = request.form["amount"]
        email = session['email']

        stmt = ibm_db.prepare(connection, "INSERT INTO expenses VALUES (?,?,?,?,?)")
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.bind_param(stmt, 2, expense)
        ibm_db.bind_param(stmt, 3, date)
        ibm_db.bind_param(stmt, 4, expense_type)
        ibm_db.bind_param(stmt, 5, amount)
        ibm_db.execute(stmt)

        return redirect(url_for("expenses"))


def format_date(date):
    return date[-2:] + "-" + date[5:7] + "-" + date[:4]


if _name_ == '_main_':
    app.run(debug=True)
