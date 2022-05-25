from crypt import methods
from flask import Flask, redirect, render_template , request, url_for
from flask_login import UserMixin,login_required,logout_user,LoginManager,current_user,login_user
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import Column,Integer,String,ForeignKey
import pymysql

engine = create_engine("mysql+pymysql://root:password@localhost/users")
Base = declarative_base()
session = Session(bind = engine, expire_on_commit = False)

class users(Base,UserMixin):
    __tablename__ = "users"
    id = Column(Integer,primary_key = True ,unique = True)
    email = Column(String)
    password = Column(String)
    role_id = Column(Integer)

# Base.metadata.create_all()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkey'

login_manager = LoginManager(app)
login_manager.login_view = '/'

@login_manager.user_loader
def load_user(id):
    return session.query(users).get(id)


def check_user(role_id):
    if role_id == 0:
        return True
    else:
        return False
    

@app.route('/',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        check = session.query(users).filter(users.email == email).first()
        if check.password == password:
            login_user(check,remember = True)
            return redirect(url_for("home"))
        else:
            return 'Login Failed'
    return render_template('login.html')

@app.route('/homne',methods = ['GET'])
@login_required
def home():
    user = current_user
    role = check_user(current_user.role_id)
    if role:
        return render_template('home.html',user = current_user),200
    else:
        return 'Not Authorised' , 401

if __name__ == "__main__":
    app.run(debug = True)