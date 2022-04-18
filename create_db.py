from ctypes import c_longdouble
import dataset
from sqlalchemy import create_engine
from sqlalchemy import Column,Integer,String,Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import Flask, request, flash, url_for, redirect, render_template
from sqlalchemy import create_engine

from flask_sqlalchemy import SQLAlchemy


# Create Table:
origin = [ 
             {
                'id':1,
                'name':'an',
                'gender':'female',
                'age':'18~25',
                'club member' : 'active',
                'fashion news frequency': 'none'
            }
        ]
sqlite_db='sqlite:///DevDb.db'
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = [DB_TYPE]+[DB_CONNECTOR]://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DevDb.db'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

##  create a database with item from data
def create(data):
    # engine = create_engine(sqlite_db, echo=True)
   # 定義資料庫的DataFrame
    # base = declarative_base()

    #使用FLASK定義
    base = db.Model
            
    class AppInfo(base):
        __tablename__ = 'app_info'

        id = db.Column('id',db.Integer, primary_key=True)
        name = db.Column(db.String)
        gender = db.Column(db.String)
        age = db.Column(db.String)
        club = db.Column(db.String)
        fnews = db.Column(db.String)

        def __init__(self,name, gender, age,club,fnews):
            self.name = name
            self.gender = gender
            self.age = age
            self.club = club
            self.fnews = fnews
    # 產生資料表
    # base.metadata.create_all(engine)
    db.create_all()

    # Session = sessionmaker(bind=engine)
    # session = Session()

    # item = [AppInfo(**i) for i in data]
    # session.add_all(item)
    # session.commit()
    item =AppInfo(name='test',gender='Male',age='18~25',club='Activate',fnews='None')
    db.session.add(item)
    db.session.commit()


create(origin)
# db= dataset.connect(sqlite_db)
# print( list(db['app_info']) )
