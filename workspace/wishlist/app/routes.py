from main import app, render_template, request, User, session, url_for, redirect
import sqlite3
from flask import jsonify



    

@app.route('/')
def home(error=None):
    title="Home"
    return render_template("home.html",title=title,error=error)
	

@app.route('/api/thumbnail/process/', methods=['GET'])
def thumbnail():
    """Retrieve Thumbnail for item added to wishlist"""
    return "Thumbnail processing"
    
    
@app.route('/api/user/register/', methods=['GET','POST'])
def register(name=None):
    """ Adds a new user to the wishlist user base"""
    title="Register"
    error=None
    if request.method == "GET":
        return render_template("register.html",title=title)
    if request.method == "POST":
        print "method is post"
        if request.form['firstname']=="" or request.form['lastname'] =="" or request.form['email']=="" or request.form['password'] =="" or request.form['password_conf'] =="":
            error="Invalid User Info Supplied"
            print error
        else:
            try:
                
                if request.form['password'] !=request.form['password_conf']:
                    error ="passwords dont match"
                else:
                    created_user = User(request.form['firstname'].upper(),request.form['lastname'].upper(),request.form['email'].lower(),request.form['password'].upper())
                   
                    conn = sqlite3.connect(app.config['DATABASE'])
                    if conn is not None:
                        cur = conn.cursor()
                        cur.execute("SELECT * from wishlist_users where email=?",(created_user.email))
                        row = cur.fetchone()
                        if row is None:
                            cur.execute("INSERT INTO wishlist_users (firstname,lastname,email,password) VALUES (?,?,?,?)", (created_user.firstname, created_user.lastname, created_user.email, created_user.password) )
                            conn.commit()
                        else:
                            raise ValueError
                        print created_user.firstname
                    error= "User Created Successfully! Please go to login page"
            except:
                error="Registration Failed"
        return render_template("register.html",title=title,error=error)
    

def valid_login(mail,passw):
    try:
        conn = sqlite3.connect(app.config['DATABASE'])
        print "connection"
        if conn is not None:
            
            cur = conn.cursor()
            
            cur.execute("SELECT * from wishlist_users where email=? and password=?",(mail.lower(),passw))
            row = cur.fetchone()
            print "fetched"
            if row is not None:
                print "row not none"
                return True
            else:
                raise ValueError
    except:
        return False
    
def log_the_user_in(mail):
    uid=None
    try:
        conn = sqlite3.connect(app.config['DATABASE'])
        print "Got here login user"
        if conn is not None:
            print "connection in login user"
            cur = conn.cursor()
            print "cursor in login user"+mail
            cur.execute("SELECT * from wishlist_users where email=?",[mail])
            print "Got here"
            row = cur.fetchone()
            if row is not None:
                print "Got here"
                uid=row[0]
                print "fetched wishlist"
                session['email'] = request.form['email']
                print "fetched wishlist"
                cur.execute("SELECT * from wishlist_set where id=?",[uid])
                wish_list = cur.fetchall()
                
                return redirect(url_for('view_list', uid=uid,wish_list=wish_list))
            else:
                raise ValueError
    except:
        error="Failed to login user"
        return redirect(url_for('login', error=error))
    
    


@app.route('/api/user/login/', methods=['GET','POST'])
def login():
    """ Verifies whether or not user has access to wishlist"""
    title="Login"
    if request.method == "GET":
        return render_template("login.html",title=title)
    if request.method == "POST":
        print "inside post"
        if valid_login(request.form['email'],request.form['password']):
            print "valid user"
            return log_the_user_in(request.form['email'].lower())
        else:
            error="Failed Login"
        return render_template("login.html",title=title,error=error)
	
	
@app.route('/api/user/<int:uid>/wishlist/', methods=['GET','POST'])
def view_list(uid):
    """ Verifies whether or not user has access to wishlist"""
    error=None
    return render_template("wishlist.html",error=error)
    
@app.route('/api/user/test/', methods=['GET','POST'])
def view_test():
    """ Verifies whether or not user has access to test"""
    try:
        conn = sqlite3.connect(app.config['DATABASE'])
        print "connect done"
        if conn is not None:
            cur = conn.cursor()
            print "cursor done"
            cur.execute("SELECT * from wishlist_users")
            print "execute done"
            row = cur.fetchone()
            if row is not None:
                print "fetch done in if"
                return jsonify(uid=row[0],email=row[3],firstname=row[1],lastname=row[2])
        else:
            raise ValueError
    except:
        error="Failed to generate json"
        return render_template('home.html', error=error)
        
