from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "#someSecretString"


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner_id):
        self.title = title
        self.body = body
        self.owner_id = owner_id

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='user', lazy=True)
    

    def __init__(self, username, password, blogs):
        self.username = username
        self.password = password
        self.blogs = blogs

@app.before_request
def require_login():
    allowed_routes = ['login', 'blog', 'index', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')
        

@app.route('/', methods=['GET'])
def index():

        return render_template('login.html')



@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        if username and user.password and user.verify == password:
            session['username'] = username
            return render_template('newpost.html', title="Add a Blog Entry", newpost=newpost)



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if username and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        elif username and user.password != password:
            flash('User password is incorrect')
            return render_template('login.html')
        elif username and user.password != username:
            flash('Username does not exist')
            return render_template('login.html')
        else:
            return render_template('signup.html')

@app.route('/logout', methods=['GET'])
def logout():
    #del session['username']
    return redirect('/')
    

# The /blog route displays all the blog posts.
@app.route('/blog', methods=['POST', 'GET'])
def blog():

    blog = Blog.query.all()

    return render_template('blog.html', title="Build a Blog", blog=blog)

# You're able to submit a new post at the /newpost route. 

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():


    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()

        return redirect('/blog')
    
    else:
        return render_template('newpost.html')

@app.route('/singleuser', methods=['POST', 'GET'])
def singleuser():


    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()

        return redirect('/blog')
    
    else:
        return render_template('singleuser.html')


if __name__ == '__main__':
    app.run()

    