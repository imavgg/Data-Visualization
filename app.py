from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

import numpy as np
from sqlite3 import connect
import json,pickle,os,csv
import pandas as pd
from pyparsing import col

# Save the AI MODEL INFO
from Model_1 import pickle_model  as x2art # x2articles
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

class Appmail():
    def __init__(self, title, sender, body):
        self.title = title
        self.sender = sender
        self.body = body

# add user input item into database
class AppInfo(db.Model):
    # 定義DB column
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

    def predict(self, predict):
        self.PREDICT=predict
# main link
@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('data/show_all.html', appInfo=AppInfo.query.all())


# 推薦產品 ML1
@app.route('/recommend', methods=['GET','POST'])
def recommend():
    # rec 位動作的頁面   
    # 接收UI輸入
    if request.method == 'POST':  # pass with ULR   
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
            # run ML
            ex1 =x2art.encode(info)
            y1 = x2art.predict(ex1) 
                 
            # save to db
            info.predict(str(y1))
            db.session.add(info)
            db.session.commit()

            # 導入至推薦產品頁面
            flash('Record was successfully added')
            return render_template('data/rec.html', prediction_text='{}.jpg'.format(y1))

    return render_template('data/rec.html')


# 推薦產品 ML2:傳回給customer的圖片 
@app.route('/recommend2', methods=['GET','POST'])
def recommend2():
    global customer
    # init
    customer='cus_1'

    # get customer id, and 傳入Customer ID 的圖
    # slt1 = request.form.get('cus_ID')
    if not request.form.get('cus_ID')==  None:

        # articles for customer ID
        articles = ft.cus_id(request.form.get('cus_ID'))
        print('articles for customer ID=',articles)
        customer = request.form.get('cus_ID') #customer 回傳給 global variable

        # articles ID pictures location
        lls = []
        # articles ID pictures
        FNs=[]
        for DXX in articles:
            N = str(DXX)
            F = 'item2'
            FN = F +'\\'+ N
            FFN = os.path.join(app.config['CLOTHS_FOLDER'],FN)
            FFN = FFN + '.jpg'
            lls.append(FFN)
            FNs.append(N)
            
        # print(lls) 
        # 傳回給checkbox的圖片
        return render_template('data/rec_ML2.html',cus_text=customer,atcl_text=lls,arts=FNs,atc1=articles)
    

    checked = request.form.getlist('article')    
    if checked ==[] or customer==None:
        pass
    else:
        x=ft.lgbm()
        y=ft.RandomForest()
        z=ft.xgboost()

        # print("checked:",checked)
        print("cus:",customer)

        product = ft.predict(x,y,z,customer,checked)
        
        return render_template('data/rec_ML2.html',prediction_text=product,cus_text=customer)

    return render_template('data/rec_ML2.html',articles)


        
   

    


# 依照各FORM ID  連結去推薦產品頁面
@app.route('/backend/<app_id>')
def modify(app_id):
    if request.method == 'GET':  
        if not app_id:
            flash('Please enter the fields', 'error')
        else:
            # 從資料庫撈出某一欄位顧客資訊
            info = db.session.query(AppInfo).filter_by(id=app_id).first()            
            y1 = info.PREDICT        
            return render_template('data/rec.html', prediction_text='{}.jpg'.format(y1))
            
@app.route('/backend')
def back():
    return render_template('data/rec_ML1.html', appInfo=AppInfo.query.all())



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


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
