from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "#someSecretString"

#setup a Blog class

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/', methods=['GET'])
def index():

    return render_template('newpost.html')

# The /blog route displays all the blog posts.
@app.route('/blog', methods=['POST', 'GET'])
def blog():

    blogs = Blog.query.all()

    return render_template('blog.html', title="Build a Blog", blogs=blogs)

# You're able to submit a new post at the /newpost route. After submitting a new post, 
# your app displays the main blog page.

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




if __name__ == '__main__':
    app.run()

    