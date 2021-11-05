from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# Reference: https://flask.palletsprojects.com/en/2.0.x/patterns/sqlalchemy/
# /// is relative path and //// is absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sample.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

# Reference: https://flask.palletsprojects.com/en/2.0.x/quickstart/
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # Reference: https://flask.palletsprojects.com/en/2.0.x/reqcontext/
        # Add a task
        task_content = request.form['content'] # 'content' is Line 38 in index.html
        new_task = Todo(content=task_content)
        # add to db
        try:
            db.session.add(new_task)
            db.session.commit()
            # redirect to home page
            return redirect('/')
        except:
            return 'Error on adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>') # id is primary key and unique
def delete(id):
    # Reference: https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error on deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    updated_task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        updated_task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Error on updating your task'

    else:
        return render_template('update.html', task=updated_task)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
