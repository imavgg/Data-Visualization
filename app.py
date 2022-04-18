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
import pickle_model0  as xdart # x2articles
CLOTHS_FOLDER = os.path.join('static','cloths')
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = [DB_TYPE]+[DB_CONNECTOR]://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DevDb.db'
app.config['CLOTHS_FOLDER'] = CLOTHS_FOLDER
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)
mail = Mail(app)
class Appmail():
    def __init__(self,title,sender,body):
        self.title= title
        self.sender = sender
        self.body = body

# add item into database
class AppInfo(db.Model):
    id = db.Column('id',db.Integer, primary_key=True)
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

    def __init__(self,sales_channel_id,product_group_name,
    graphical_appearance_name,colour_group_name,section_name,garment_group_name,
    Year,season,pricelabel,salelabel,PREDICT):
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
    if request.method == 'POST':
        if not request.form['sales_channel_id'] or not request.form['product_group_name'] or not request.form['graphical_appearance_name']:
            flash('Please enter all the fields', 'error')
        else:
            # 從 HTML 得到參數 並 新增info欄位
            info = AppInfo(request.form['sales_channel_id'],
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
            db.session.add(info)
            db.session.commit()
            flash('Record was successfully added')'''
    return render_template('data/show_all.html')

#視覺化
@app.route('/vis',methods=['GET', 'POST']) 
def visualization():
    return render_template('data/vis.html', appInfo=AppInfo.query.all())

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

# 推薦產品頁面
@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    '''
    # 這裡引入folder 內圖檔
    from random import sample #假裝是機器學習 XDD
    ls = ['0108775015','0108775044','0108775051','0110065001','0110065002','0110065011','0111565001','0111565003','0111586001','0111593001','0111609001','0112679048','0112679052','0114428026','0114428030','0116379047','0118458003','0118458004','0118458028','0118458029','0118458034','0118458038','0118458039']
    lls = []
    R = sample(ls,12)
    for DXX in R:
        N = str(DXX) + '.jpg'
        F = str(DXX)[0:3]
        FN = F +'/'+ N
        lls.append(FN)
    B = lls
    #B = 'an'+'/'+'test'+'.jpg' #無須另加''  (= = 搞到我呀~小哥哥)
    print("B =",B)
    #files = os.path.join(app.config['CLOTHS_FOLDER'],'an/test.jpg')
    files1 = os.path.join(app.config['CLOTHS_FOLDER'],B[0])
    files2 = os.path.join(app.config['CLOTHS_FOLDER'],B[1])
    files3 = os.path.join(app.config['CLOTHS_FOLDER'],B[2])
    files4 = os.path.join(app.config['CLOTHS_FOLDER'],B[3])
    files5 = os.path.join(app.config['CLOTHS_FOLDER'],B[4])
    files6 = os.path.join(app.config['CLOTHS_FOLDER'],B[5])
    files7 = os.path.join(app.config['CLOTHS_FOLDER'],B[6])
    files8 = os.path.join(app.config['CLOTHS_FOLDER'],B[7])
    files9 = os.path.join(app.config['CLOTHS_FOLDER'],B[8])
    files10 = os.path.join(app.config['CLOTHS_FOLDER'],B[9])
    files11 = os.path.join(app.config['CLOTHS_FOLDER'],B[10])
    files12 = os.path.join(app.config['CLOTHS_FOLDER'],B[11])
    '''
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
        N = str(DXX)
        F = str(DXX)[0:3]
        FN = F +'\\'+ N
        lls.append(FN)
    B = lls
    #y1 = y1[0]
    y1 = os.path.join(app.config['CLOTHS_FOLDER'],B[0])
   
    return render_template('data/rec.html', prediction_text='{}.jpg'.format(y1))



# 依照各ID  連結去推薦產品頁面
@app.route('/predict/<app_id>', methods=['GET', 'POST'])
def modify(app_id):
    if request.method == 'GET':  
        if not app_id:
            flash('Please enter the fields', 'error')
        else:
            # 從資料庫撈出產品
            appInfo = db.session.query(AppInfo).filter_by(id=app_id).first()
            print('appInfo.name = ',appInfo.name)
            print('appInfo.Gender = ',appInfo.gender)
            print('appInfo.Age = ',appInfo.age)
            print('appInfo.Club = ',appInfo.club)
            print('appInfo.Fashion News = ',appInfo.fnews)
            print(type(appInfo.age))

            #print('appInfo =',appInfo)
            flash('Record was successfully delete')
    return redirect(url_for('recommend'))




if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
