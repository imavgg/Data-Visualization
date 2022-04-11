from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import os
from sqlite3 import connect

import json
import pandas as pd

CLOTHS_FOLDER = os.path.join('static', 'cloths')
JSON_FOLDER = os.path.join('static', 'data')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DevDb.db'
app.config['CLOTHS_FOLDER'] = CLOTHS_FOLDER
app.config['SECRET_KEY'] = "random string"
app.config['JSON_FOLDER'] = JSON_FOLDER
db = SQLAlchemy(app)
mail = Mail(app)

# 輸入json
data_folder = app.config['JSON_FOLDER']
file1 = open(JSON_FOLDER+'\\garment_group_name.json')
file2 = open(JSON_FOLDER+'\\perceived_colour_value_name'+'.json')
file_a = open(JSON_FOLDER+'\\index_color'+'.json')
file_b = open(JSON_FOLDER+'\\index_category'+'.json')
data1 = json.load(file1)
data2 = json.load(file2)
tran1 = json.load(file_a)
tran2 = json.load(file_b)


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

    def __init__(self, name, gender, age, club, fnews):
        self.name = name
        self.gender = gender
        self.age = age
        self.club = club
        self.fnews = fnews


class AppML(AppInfo):

    def model(self):
        self.out = 'test'+'.jpg'
        return(self.out)


# main link
@app.route('/', methods=['GET', 'POST'])
def main_page():
    # 接收UI輸入
    if request.method == 'POST':  # pass with http
        if not request.form['name'] or not request.form['gender'] or not request.form['age']:
            flash('Please enter all the fields', 'error')
        else:
            # 新增AppInfo欄位的客戶進入db
            info = AppInfo(request.form['name'],
                           request.form['gender'],
                           request.form['age'],
                           request.form['club'],
                           request.form['fnews']
                           )
            db.session.add(info)
            db.session.commit()
            flash('Record was successfully added')

            # return redirect(url_for('main_page'))
    return render_template('data/show_all.html', appInfo=AppInfo.query.all())


@app.route('/db2json')
def db2json():
    # read sql     include UI顧客database資訊
    df = pd.read_sql('app_info', 'sqlite:///DevDb.db')
    
    # 這是一個column count
    tab_gender = df.groupby(['gender']).sum()
    # 轉成 json
    # for loop(1:) in key 寫成一個大 json
    # 做成一個大json:包含全部有 table column group count, 
    # GOAL: {"fashion": 
    #  [
    #      {
    #        "column": "fashion",
    #        "number": "5"
    #      },
    #      {
    #        "column": "not fashion",
    #        "number": "1"
    #      }
    #  ],"gender": 
    #  [
    #      {
    #        "column": "male",
    #        "number": "2"
    #      },
    #      {
    #        "column": "female",
    #        "number": "4"
    #      }
    #  ]}
    # retun json
    js = jsonify(df.to_dict(orient='records'))
    return(js)


# 新增一個後端管理站 需要輸入帳號密碼為ROOT權限才可啟用開啟資料庫的管理介面
# 介面包含"使用者輸入進db的總數量,使用者類別等等
@ app.route('/root', methods=['GET', 'POST'])
def root():
    if request.method == 'POST':
        if not (request.form['uname'] == 'root' and request.form['psw'] == 'root'):
            print('login false')
            return render_template('data/login.html', login=False)
        else:
            # 從root html 收到 x值
            x = request.args.get('x')
            return render_template('data/root.html', appInfo=AppInfo.query.all(), args=[x])
    return render_template('data/login.html')


# 視覺化接收選單name
@ app.route('/vis', methods=['GET', 'POST'])
def visualization():
    data_js = 0
    data_js2 = 0


    if request.method == 'POST':
       
        # import file
        if request.form['pie'] == 'garment_group_name' and request.form['bar'] == 'index_color':
            data_js = data1
            data_js2 = file1

            print("get pie1,bar1")
        elif request.form['pie'] == 'garment_group_name' and request.form['bar'] == 'index_category':
            data_js = data1
            data_js2 = file2
            print("get pie1,bar2")

        elif request.form['pie'] == 'perceived_colour_value_name' and request.form['bar'] == 'index_color':
            data_js = data2
            data_js2 = file1
            print("get pie2,bar1")
        elif request.form['pie'] == 'perceived_colour_value_name' and request.form['bar'] == 'index_category':
            data_js = data2
            data_js2 = file2
            print("get pie2,bar2")
        else:
            print("nothing")
        
    return render_template('data/vis.html', jsfile=data_js, jsfile2=data_js2)


# 關於我們
@ app.route('/us', methods=['GET', 'POST'])
def us():
    if request.method == 'POST':
        if not request.form['title'] or not request.form['sender']:
            flash('Please enter all the fields', 'error')
        else:
            mail = Appmail(request.form['title'],
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
    # OS這裡引入folder + ml_result(test.jpg)
    files = os.path.join(app.config['CLOTHS_FOLDER'])
    file = files+"\\test.jpg"
    print(file)

    # rec html 讀取files
    return render_template('data/rec.html', recommend_images=file, appInfo=AppInfo.query.all())


@app.route('/recommend/<ml_result>', methods=['GET', 'POST'])
def recommend_cus(ml_result):
    if request.method == 'GET':
        if not ml_result:
            flash('Please enter the fields', 'error')
        else:
            # OS這裡引入folder + ml_result(test.jpg)
            files = os.path.join(app.config['CLOTHS_FOLDER'], ml_result)
            print(files)
            # rec html 讀取files
            return(files)
    return render_template('data/rec.html', recommend_images=files, appInfo=AppInfo.query.all())


# 依照各ID  連結去推薦產品頁面
@app.route('/predict/<app_id>', methods=['GET', 'POST'])
def modify(app_id):
    if request.method == 'GET':
        if not app_id:
            flash('Please enter the fields', 'error')
        else:
            # 從資料庫撈出產品
            # 1.2.3....
            appInfo = db.session.query(AppInfo).filter_by(id=app_id).first()
            ml_result = AppML.model(appInfo)  # test.jpg
            print(ml_result)
            app.config['RECOMMEND_RESULT'] = ml_result

    return redirect(url_for('recommend_cus', ml_result=ml_result))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
