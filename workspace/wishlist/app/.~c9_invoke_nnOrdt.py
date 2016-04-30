from main import app, render_template, request, User

@app.route('/')
def home(name=None):
    title="Home"
    return render_template("home.html",title=title)
	

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
        print request.form['firstname']
        if request.form['firstname']=="" or request.form['lastname'] =="" or request.form['email']=="" or request.form['password'] =="" or request.form['password_conf'] =="":
            error="Invalid User Info Supplied"
        created_user = User(request.form['firstname'],request.form['lastname'],request.form['email'],request.form['password'])
        print created_user
        if created_user == "<User ''>":
            
            print error
        return render_template("register.html",title=title,error=error)
    
    
@app.route('/api/user/login/', methods=['GET','POST'])
def login():
    """ Verifies whether or not user has access to wishlist"""
    title="Login"
    if request.method == "GET":
        return render_template("login.html",title=title)
    if request.method == "POST":
        request.form['']
        return render_template("login.html",title=title)
	
	
@app.route('/api/user/:id/wishlist/', methods=['GET','POST'])
def view_list():
    """ Verifies whether or not user has access to wishlist"""
    return "wishlist"