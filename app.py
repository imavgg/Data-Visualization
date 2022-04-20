from tkinter import Y
from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import os
import numpy as np
from sqlite3 import connect
import json,pickle
import pandas as pd
from pyparsing import col
from Model_1 import pickle_model  as x2art # x2articles
from Model_1 import pickle_model0  as xdart # x2articles
from Model_2 import for_test as ft #另一組 推薦系統


CLOTHS_FOLDER = os.path.join('static', 'cloths')
JSON_FOLDER = os.path.join('static', 'data')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DevDb.db'
app.config['CLOTHS_FOLDER'] = CLOTHS_FOLDER
app.config['SECRET_KEY'] = "random string"
app.config['JSON_FOLDER'] = JSON_FOLDER
db = SQLAlchemy(app)
mail = Mail(app)


# this is a test for printing images on recommend
prediction =[]
def test():
    from random import sample 
    # The default random articles ID for ML
    IDs = ['0108775015','0108775044','0108775051','0110065001','0110065002','0110065011','0111565001','0111565003','0111586001','0111593001','0111609001','0112679048','0112679052','0114428026','0114428030','0116379047','0118458003','0118458004','0118458028','0118458029','0118458034','0118458038','0118458039']
    cloth_files=[]
    picked = sample(IDs,12)
    for DXX in picked:
        Name = str(DXX) + '.jpg'
        Folder = str(DXX)[0:3]
        FN = Folder +'\\'+ Name
        cloth_files.append(FN)

    # return 給HTML的參數
    files=[]
    for i in cloth_files:
        file = app.config['CLOTHS_FOLDER']+ '\\'+ i
        # print(file)
        files.append(file)
    return(files)
files = test()

class Appmail():
    def __init__(self, title, sender, body):
        self.title = title
        self.sender = sender
        self.body = body

# add user input item into database
class AppInfo(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String)
    gender = db.Column(db.String)
    age = db.Column(db.String)
    club = db.Column(db.String)
    fnews = db.Column(db.String)

    # FOR MODEL1
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
    PREDICT = db.Column(db.String) #save predict result

    # FOR MODEL2

    def __init__(self, name, gender, age, club, fnews,sales_channel_id,
    product_group_name,graphical_appearance_name,colour_group_name,
    section_name,garment_group_name,Year,season,pricelabel,salelabel,PREDICT):
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
        self.PREDICT=PREDICT

# main link
@app.route('/', methods=['GET', 'POST'])
def main_page():
    '''
    # 接收UI輸入
    if request.method == 'POST':  # pass with http
        if not request.form['name'] or not request.form['gender'] or not request.form['age']:
            flash('Please enter all the fields', 'error')
        else:
            # 從 HTML 得到參數 並 新增info欄位
            info = AppInfo(request.form['name'],
                           request.form['gender'],
                           request.form['age'],
                           request.form['club'],
                           request.form['fnews'],
                           request.form['sales_channel_id'],
                           request.form['product_group_name'],
                           request.form['graphical_appearance_name'],
                           request.form['colour_group_name'],
                           request.form['section_name'],
                           request.form['garment_group_name'],
                           request.form['Year'],
                           request.form['season'],
                           request.form['pricelabel'],
                           request.form['salelabel'],
                           'NONE'
                           )
            # 加進DB
            db.session.add(info)
            db.session.commit()
            flash('Record was successfully added')'''
    #return render_template('data/show_all.html', appInfo=AppInfo.query.all())
    return render_template('data/show_all.html')


# Restful接收data
@app.route('/data_pie')
def data_pie():
        
    # 輸入json
    file1 = open(JSON_FOLDER+'\\garment_group_name.json')
    file2 = open(JSON_FOLDER+'\\perceived_colour_value_name'+'.json')
    
    data1 = json.load(file1)
    data2 = json.load(file2)
    #  判別 html 傳回的plot columns項目
    pie = request.args.get('pie')
    data_js=data1
    # import file
    if pie == 'garment_group_name':
        data_js = data1

    elif pie == 'perceived_colour_value_name':
        data_js = data2

    else:
        print("nothing")
    # ?/data_pie?pie=garment_group_name  ---> return data.js
    # return a string. 
    return( json.dumps(data_js))

@app.route('/data_bar')
def data_bar():
        
    file1 = open(JSON_FOLDER+'\\bar\\index_group_perceived_colour_value_name'+'.json')
    file2 = open(JSON_FOLDER+'\\bar\\index_group_product_group_name'+'.json')
    data1 = json.load(file1)
    data2 = json.load(file2)
    #  判別 html 傳回的plot columns項目    
    bar = request.args.get('bar')
    print('bar',bar)
    data_js=data1
    # import file
    if bar == 'index_group_product_group_name':
        data_js = data2
    elif bar == 'index_group_perceived_colour_value_name':
        data_js = data1
    else:
        print("nothing")
    return( json.dumps(data_js))

@app.route('/data_timeline')
def data_timeline():
        
    file1 = open(JSON_FOLDER+'\\time\\dateprice.json')
    file2 = open(JSON_FOLDER+'\\time\\dattoaccu.json')
    data1 = json.load(file1)
    data2 = json.load(file2)
    #  判別 html 傳回的plot columns項目    
    timeline = request.args.get('timeline')
    print('timeline',timeline)
    data_js=data1
    # import file
    if timeline == 'dateprice':
        data_js = data1
    elif timeline == 'dattoaccu':
        data_js = data2
    else:
        print("nothing")
    return( json.dumps(data_js))

# 視覺化接收選單name
@ app.route('/vis', methods=['GET', 'POST'])
def visualization():
    
    pie = request.args.get('pie')
    bar = request.args.get('bar')  
    timeline = request.args.get('timeline')    
    globalc = request.args.get('globalc')
    
    return render_template('data/vis.html', args=[pie,bar,timeline,globalc] )
# 關於我們
@app.route('/us',methods=['GET', 'POST'])
def us():
    if request.method == 'POST':        
        if not request.form['title'] or not request.form['sender']:
            flash('Please enter all the fields', 'error')
        else:
            mail = Appmail( request.form['title'], 
                            request.form['sender'],
                           request.form['body']
                           )
            msg_recipients = ['applean061516@gmail.com']
            msg = Message(mail.title,
                sender=mail.sender,
                recipients=msg_recipients,
                body=mail.body)
            mail.send(msg)
            return('Mail sent')

    return render_template('data/us.html', appInfo=AppInfo.query.all())

@app.route('/recommend_popular')
def recommend_popular():
    #推薦最受歡迎的
    return render_template('data/rec.html')

# 推薦產品頁面
@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    # rec html 讀取files
    select1 = request.form.get('sales_channel_id')
    select2 = request.form.get('product_group_name')
    select3 = request.form.get('graphical_appearance_name')
    select4 = request.form.get('colour_group_name')
    select5 = request.form.get('section_name')
    select6 = request.form.get('garment_group_name')
    select7 = request.form.get('Year')
    select8 = request.form.get('season')
    select9 = request.form.get('pricelabel')
    select0 = request.form.get('salelabel')

    ex1 =xdart.encode(select1,select2,select3,select4,select5,select6,select7,select8,select9,select0)
    y1 = xdart.predict(ex1)  #這是arrary
    lls = []
    for DXX in y1:
        N = '0'+str(DXX)
        F = 'item'
        FN = F +'\\'+ N
        lls.append(FN)
    B = lls
    #y1 = y1[0]
    y1 = os.path.join(app.config['CLOTHS_FOLDER'],B[0])
    return render_template('data/rec.html', prediction_text='{}.jpg'.format(y1))

#另一組的推薦_首頁
@app.route('/recommend0_f')
def recommend0_f():

    return render_template('data/rec_f.html')

#另一組的推薦
@app.route('/recommend0', methods=['GET', 'POST'])
def recommend0():
    slt1 = request.form.get('cus_ID')
    if request.form.get('cus_ID') == None:
        slt1 = '1'
    atcl = ft.cus_id(slt1)
    slt1 =  "Customer_ID : " + slt1
    #atcl = str(atcl)
    lls = []
    for DXX in atcl:
        N = str(DXX)
        F = 'item2'
        FN = F +'\\'+ N
        FFN = os.path.join(app.config['CLOTHS_FOLDER'],FN)
        FFN = FFN + '.jpg'
        lls.append(FFN)
    B = lls
    return render_template('data/rec0.html',cus_text=slt1,atcl_text=B)

# 依照各FORM ID  連結去推薦產品頁面
@app.route('/recommend/<app_id>', methods=['GET', 'POST'])
def modify(app_id):
    if request.method == 'GET':  
        if not app_id:
            flash('Please enter the fields', 'error')
        else:
            # 從資料庫撈出某一欄位顧客資訊
            appInfo = db.session.query(AppInfo).filter_by(id=app_id).first()

            # AI Model 1 :產生一個article id
            ex1 =x2art.encode(appInfo)
            y1 = x2art.predict(ex1)         

            # save to model
            appInfo.PREDICT =str(y1)
            db.session.add(appInfo)    
            db.session.commit()
   

    return render_template('data/rec.html', prediction_text='{}.jpg'.format(y1))



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
