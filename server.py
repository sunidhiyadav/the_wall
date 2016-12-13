from flask import Flask, render_template, request,  make_response, redirect, session, flash, url_for
import re
from flask_bcrypt import Bcrypt
from mysqlconnection import MySQLConnector

app = Flask(__name__)
app.secret_key = 'ThisIsSecret'
mysql = MySQLConnector(app, 'walldb')
bcrypt = Bcrypt(app)

emailRegex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
passwordRegex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')


def validate():
    errors = 0
    #Check first name
    if request.form['first_name'] == '':
        flash('Name cannot be blank', 'firstNameError')
        errors += 1
        pass
    elif any(char.isdigit() for char in request.form['first_name']) == True:
        flash('Name cannot have numbers', 'firstNameError')
        errors += 1
        pass
    else:
        session['first_name'] = request.form['first_name']
 
    #Check last name
    if request.form['last_name'] == '':
        flash('Name cannot be blank', 'lastNameError')
        errors += 1
        pass
    elif any(char.isdigit() for char in request.form['last_name']) == True:
        flash('Name cannot have numbers', 'lastNameError')
        errors += 1
        pass
    else:
        session['last_name'] = request.form['last_name']

    #Check email
    if request.form['email'] == '':
        flash('Email cannot be blank', 'emailError')
        errors += 1
        pass
    elif not emailRegex.match(request.form['email']):
        flash('Invalid email address', 'emailError')
        errors += 1
        pass
    else:
        session['email'] = request.form['email']

    #Check password
    if request.form['password'] == '':
        flash('Password cannot be blank', 'passwordError')
        errors += 1
        pass
    elif len(request.form['password']) < 8:
        flash('Password must be greater than 8 characters', 'passwordError')
        errors += 1
        pass
    elif not passwordRegex.match(request.form['password']):
        flash('Password must contain at least one lowercase letter, one uppercase letter, and one digit', 'passwordError')
        errors += 1
        pass
    else:
        session['password'] = request.form['password']

    #Check confirmation password
    if request.form['confirm_password'] == '':
        flash('Please confirm password', 'confirmPasswordError')
        errors += 1
        pass
    elif request.form['confirm_password'] != request.form['password']:
        flash('Passwords do not match', 'confirmPasswordError')
        errors += 1
    else:
        session['confirm_password'] = request.form['confirm_password']

    #See if there are any errors
    if errors > 0:
        session['password'] = ''
        session['confirm_password'] = ''
        return False
    else:
        return True

def validateLogin():
    errors = 0
     #Check email
    if request.form['email'] == '':
        flash('Email cannot be blank', 'emailError')
        errors += 1
        pass
    elif not emailRegex.match(request.form['email']):
        flash('Invalid email address', 'emailError')
        errors += 1
        pass
    else:
        session['email'] = request.form['email']

    #Check password
    if request.form['password'] == '':
        flash('Password cannot be blank', 'passwordError')
        errors += 1
        pass
    elif len(request.form['password']) < 8:
        flash('Password must be greater than 8 characters', 'passwordError')
        errors += 1
        pass
    elif not passwordRegex.match(request.form['password']):
        flash('Password must contain at least one lowercase letter, one uppercase letter, and one digit', 'passwordError')
        errors += 1
        pass
    else:
        session['password'] = request.form['password']

        #See if there are any errors
    if errors > 0:
        session['password'] = ''
        session['confirm_password'] = ''
        return False
    else:
        return True


def checkForExistingEmail():
    query = "SELECT email FROM users WHERE email = :email"
    data={'email' :request.form['email']}
    email = mysql.query_db(query,data)
    if email: 
        return False
    else:
        return True

@app.route('/')
def index():
    if not session.get('email'):
        session['email'] = ''
        return render_template('index.html')
    if not session.get('password'):
        session['password'] = ''   
        return render_template('index.html')

    if session['email'] != '':
        return redirect('/wall')

@app.route('/register')
def register():
    if not session.get('first_name'):
        session['first_name'] = ''
    if not session.get('last_name'):
        session['last_name'] = ''
    if not session.get('email'):
        session['email'] = ''
    if not session.get('password'):
        session['password'] = ''
    if not session.get('confirm_password'):
        session['confirm_password'] = ''
    return render_template('register.html')

    if session['first_name'] != '':
        return redirect('/wall') 

@app.route('/create', methods=['POST'])
def create():
    if session['first_name'] != '':
        return redirect('/wall')
         
    if validate() == False:
        return redirect('/register')
    else:
        if checkForExistingEmail() == True:
            encryptedPassword = bcrypt.generate_password_hash(request.form['password'])
            query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES ('{}', '{}', '{}','{}', NOW(), NOW())".format(session['first_name'], session['last_name'], session['email'], encryptedPassword)
            mysql.query_db(query)
            session['password'] = ''
            session['confirm_password'] = ''
            return redirect('/wall')
        else:
           flash('Account with email already exists. Please use another email', 'emailError')
           return redirect('/register') 



@app.route('/login')
def login():
     if session['first_name'] != '':
         return redirect('/wall')
     else:
         return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validateLoginInfo():
    if validateLogin() == False:
        return redirect('/')
    else:
        query ="SELECT * FROM users WHERE email = '{}'".format(session['email'])
        userInfo=mysql.query_db(query)
        #inputPassword = request.form['password']
        password = request.form['password']
        print password          

        if userInfo and bcrypt.check_password_hash(userInfo[0]['password'], password):
            print userInfo[0]['password'] 
            session['first_name'] = userInfo[0]['first_name']
            session['last_name'] = userInfo[0]['last_name']
            return redirect('/wall')
        else:
            flash('Incorrect password', 'passwordError')
    return redirect('/login')

@app.route('/wall')
def returnWall(): 
    if not session.get('user_id'):
        session['user_id'] = '' 
    if session['email']:
        query ="SELECT * FROM users WHERE email = '{}'".format(session['email'])
        userInfo=mysql.query_db(query)
        if userInfo:
           session['user_id'] = userInfo[0]['id']
           query1 ="SELECT p.post, p.id, p.user_id, date_format(p.created_at,'%D-%M-%Y %H:%I') as created_at, u.first_name from posts p inner join  users u on p.user_id =u.id"
           messageList=mysql.query_db(query1)
           query2="SELECT c.comment,c.id as cid, c.post_id,c.user_id, date_format(c.created_at, '%D-%M-%Y %H:%I') as created_at, p.id, p.post, u.first_name  from comments c inner join  posts p on c.post_id =p.id inner join users u on c.user_id = u.id"
           commentList=mysql.query_db(query2)
           r =make_response(render_template('wall.html', messageList = messageList, commentList=commentList))
           r.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
           return r
    else:
        return redirect('/login')

@app.route('/message', methods=['POST'])
def message():
    query = "INSERT INTO posts (post, user_id,created_at,updated_at) VALUES('{}','{}',NOW(),NOW())".format(request.form['message'],session['user_id'])
    postInfo = mysql.query_db(query)
    return redirect('/wall')

@app.route('/message/<id>/delete', methods=['POST'])
def delete(id):
    print id
    query = "DELETE FROM posts WHERE user_id = :user_id and id = :message_id"
    print query
    data = {'user_id': session['user_id'],
            'message_id': id}
    mysql.query_db(query, data)

    query2 = "DELETE FROM comments WHERE  post_id = :post_id"
    print query2
    data = {'post_id': id}
    mysql.query_db(query2, data)

    return redirect('/wall') 

@app.route('/comment', methods=['POST'])
def comment():
    query = "INSERT INTO comments (comment, user_id, post_id, created_at,updated_at) VALUES('{}','{}','{}', NOW(), NOW())".format(request.form['comment'],session['user_id'],request.form['message_id'])
    commnetInfo = mysql.query_db(query)
    print commnetInfo
    return redirect('/wall')    

@app.route('/comment/<commentId>/delete', methods=['POST'])
def deleteComment(commentId):
    print commentId
    query = "DELETE FROM comments WHERE  id= :comment_id"
    data = {'comment_id': commentId}
    mysql.query_db(query, data)
    print query

    return redirect('/wall')

@app.route('/logout', methods=['POST'])
def clear():
    session['first_name'] = ''
    session['last_name'] = ''
    session['email'] = ''
    session['password'] = ''
    session['confirm_password'] = ''
    session['user_id'] =''

    return redirect('/login')

app.run(debug=True)