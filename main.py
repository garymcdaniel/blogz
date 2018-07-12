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

# The /blog route displays all the blog posts.
@app.route('/blog', methods=['POST', 'GET'])
def blog():

    if request.method == 'POST':
        task_name = request.form['blog']
        new_task = Task(task_name)
        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.filter_by(completed=False).all()
    completed_tasks = Task.query.filter_by(completed=True).all()
    return render_template('blog.html',title="Build a Blog", 
        tasks=tasks, completed_tasks=completed_tasks)

# You're able to submit a new post at the /newpost route. After submitting a new post, 
# your app displays the main blog page.

@app.route('/', methods=['POST', 'GET'])
def newpost():

    task_id = int(request.form['task_id'])
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/blog')



if __name__ == '__main__':
    app.run()