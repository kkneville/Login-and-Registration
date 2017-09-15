import random, md5, re
from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = "secret"
mysql = MySQLConnector(app, 'registration')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


# def validate_login()
#     return null


@app.route('/', methods=["get", "post"])
def index():
    return render_template('index.html',)

@app.route('/errors', methods=['POST'])
def errors():

    if (len(request.form['firstname']) < 2) or (len(request.form['lastname']) < 2) :
            flash("Names must be at least 2 characters long.")
            return redirect ('/')
    if (not request.form['firstname'].isalpha) or (not request.form['lastname'].isalpha) :
            flash("Names must contain letters only.")
            return redirect ('/')
    if not EMAIL_REGEX.match(request.form['email']) :
            flash("Invalid email address.")
            return redirect ('/')
    if len(request.form['password']) < 8 :
            flash("Passwords must be at least 8 characters long.")
            return redirect ('/')
    if request.form['passwordconfirm'] != request.form['password'] :
            flash("Passwords must match.")
            return redirect ('/')
    else :
        session['firstname'] = request.form['firstname']
        session['lastname'] = request.form['lastname']
        session['email'] = request.form['email']
        session['password'] = md5.new(request.form['password']).hexdigest()
        return redirect ('/register')

@app.route('/register', methods=['POST', "GET"])
def register():
    insert_query = "INSERT into users (firstname, lastname, email, password, created_at, updated_at)  VALUES (:firstname, :lastname, :email, :password, NOW(), NOW())"
    query_data = {'firstname': session['firstname'],"lastname": session['lastname'],'email': session['email'],'password': session['password']
        }
    mysql.query_db(insert_query, query_data)

    session.pop("firstname")
    session.pop('lastname')
    session.pop('email')
    session.pop('password')

    query = "select * from users"
    users = mysql.query_db(query)

    return redirect('/success')

@app.route('/login', methods=['POST', "GET"])
def login():

    email = request.form['email']
    password = md5.new(request.form['password']).hexdigest()
    user_query = "SELECT * FROM users where users.email = :email AND users.password = :password"
    query_data = { 'email': email, 'password': password}
    user = mysql.query_db(user_query, query_data)

    return redirect ("/success")


@app.route('/success')
def success():
    return render_template ('landing.html')

app.run(debug=True)
