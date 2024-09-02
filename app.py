from flask import Flask, render_template,request ,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///task.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the Task model
class Task(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Routes
@app.route('/', methods = ['GET','POST'])
def hello_world():
    if request.method =="POST":
        title = request.form['title']
        desc = request.form['desc']
        task = Task(title = title,desc = desc)
        db.session.add(task)
        db.session.commit()
    allTask = Task.query.all()
    
    return render_template('index.html',allTask=allTask)  

    

@app.route('/update/<int:sno>',methods = ['GET','POST'])
def update(sno):
    if request.method =="POST":
        title = request.form['title']
        desc = request.form['desc']
        task = Task.query.filter_by(sno=sno).first()
        task.title = title
        task.desc = desc
        db.session.add(task)
        db.session.commit()
        return redirect("/")

    task = Task.query.filter_by(sno=sno).first()
    return render_template('update.html',task = task) 
    

@app.route('/delete/<int:sno>')
def delete(sno):
    task = Task.query.filter_by(sno=sno).first()
    db.session.delete(task)
    db.session.commit()
    return redirect("/")

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('query')
    if query:
        # Search for tasks that contain the query in the title or description
        search_results = Task.query.filter(
            Task.title.contains(query) | Task.desc.contains(query)
        ).all()
    else:
        search_results = Task.query.all()

    return render_template('index.html', allTask=search_results)


if __name__ == "__main__":
    app.run(debug=True, port=9000)
