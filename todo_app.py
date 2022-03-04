from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Topcu/Desktop/todo-app/todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(80), unique=True, nullable=False)
    # email = db.Column(db.String(120), unique=True, nullable=False)
    title = db.Column(db.String(20))
    complete = db.Column(db.Boolean) # 1- True, 0- False

@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template('index.html',todos=todos)

@app.route('/add',methods = ['POST'])
def add():
    title = request.form.get('title')
    newTodo = Todo(title = title,complete = False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<string:id>')
async def completeTodo(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.complete =  not todo.complete # true convert false, false convert true
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<string:id>')
def deleteTodo(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)