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
# origin = [ 
#              {
#                 'id':1,
#                 'name':'an',
#                 'gender':'female',
#                 'age':'18~25',
#                 'club member' : 'active',
#                 'fashion news frequency': 'none'
#             }
#         ]
sqlite_db='sqlite:///DevDb.db'
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = [DB_TYPE]+[DB_CONNECTOR]://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DevDb.db'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

##  create a database with item from data
def create():
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
            
        # sales
        sales_channel_id = db.Column(db.String)
        product_group_name= db.Column(db.String)
        graphical_appearance_name= db.Column(db.String)
        colour_group_name= db.Column(db.String)
        section_name= db.Column(db.String)
        garment_group_name= db.Column(db.String)
        Year= db.Column(db.String)
        season= db.Column(db.String)
        pricelabel= db.Column(db.String)
        salelabel= db.Column(db.String)
        PREDICT = db.Column(db.String)

    def __init__(self, name, gender, age, club, fnews,sales_channel_id,
    product_group_name,graphical_appearance_name,colour_group_name,
    section_name,garment_group_name,Year,season,pricelabel,salelabel):
        self.name = name
        self.gender = gender
        self.age = age
        self.club = club
        self.fnews = fnews
        self.sales_channel_id=sales_channel_id
        self.product_group_name=product_group_name
        self.graphical_appearance_name=graphical_appearance_name
        self.colour_group_name=colour_group_name
        self.section_name=section_name
        self.garment_group_name=garment_group_name
        self.Year=Year
        self.season=season
        self.pricelabel=pricelabel
        self.salelabel=salelabel
    # 產生資料表
    # base.metadata.create_all(engine)
    db.create_all()

    # Session = sessionmaker(bind=engine)
    # session = Session()

    # item = [AppInfo(**i) for i in data]
    # session.add_all(item)
    # session.commit()
    item =AppInfo( name='test',gender='Male',
        age='18~25',club='Activate',fnews='None',
        sales_channel_id='2',
        product_group_name='Underwear',
        graphical_appearance_name='Solid',
        colour_group_name='Yellow',
        section_name='Womens Lingerie',
        garment_group_name='Trousers',
        Year='2020',
        season='Spring',
        pricelabel='99元以下',
        salelabel='熱門')       
        
    db.session.add(item)
    db.session.commit()


create()
db= dataset.connect(sqlite_db)
print( list(db['app_info']) )
