from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///ToDo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)

class ToDo(db.Model):
    SNo=db.Column(db.Integer,primary_key=True)
    Title=db.Column(db.String(500),nullable=False)
    Desc=db.Column(db.String(1000),nullable=False)
    datecreated=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.SNo} - {self.Title}"



@app.route('/',methods=["GET","POST"])
def hello_world():
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        todo=ToDo(Title=title,Desc=desc)
        db.session.add(todo)
        db.session.commit()
        
    allToDo=ToDo.query.all()
    return render_template('index.html',allToDo=allToDo)
    #return 'Hello, World!'


@app.route('/delete/<int:SNo>')
def delete(SNo):
    todo=ToDo.query.filter_by(SNo=SNo).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:SNo>',methods=["GET","POST"])
def update(SNo):
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        todo=ToDo.query.filter_by(SNo=SNo).first()
        todo.Title=title
        todo.Desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo=ToDo.query.filter_by(SNo=SNo).first()
    return render_template('update.html',todo=todo)


if __name__=="__main__":
    app.run(debug=True)