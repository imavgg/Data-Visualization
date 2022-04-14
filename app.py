from flask import Flask, request, flash, url_for, redirect, render_template
from flask_mail import Mail,Message
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import os
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


# main link
@app.route('/', methods=['GET', 'POST'])

def main_page():
    
    if request.method == 'POST':
        if not request.form['name'] or not request.form['gender'] or not request.form['age']:
            flash('Please enter all the fields', 'error')
        else:
            # 新增AppInfo欄位的客戶進入db
            info = AppInfo( request.form['name'], 
                            request.form['gender'],
                           request.form['age'],
                           request.form['club'],
                           request.form['fnews']
                           )
            db.session.add(info)
            db.session.commit()
            flash('Record was successfully added')
            
            return redirect(url_for('main_page'))
    return render_template('data/show_all.html', appInfo=AppInfo.query.all())


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
    return render_template('data/rec.html',recommend_images1 =files1 ,recommend_images2 =files2 ,recommend_images3 =files3 ,recommend_images4 =files4 ,recommend_images5 =files5 ,recommend_images6 =files6 ,recommend_images7 =files7 ,recommend_images8 =files8 ,recommend_images9 =files9 ,recommend_images10 =files10 ,recommend_images11 =files11 ,recommend_images12 =files12 , appInfo=AppInfo.query.all())



# 依照各ID  連結去推薦產品頁面
@app.route('/predict/<app_id>', methods=['GET', 'POST'])
def modify(app_id):
    if request.method == 'GET':  
        if not app_id:
            flash('Please enter the fields', 'error')
        else:
            # 從資料庫撈出產品
            appInfo = db.session.query(AppInfo).filter_by(id=app_id).first()
            print(appInfo)
            flash('Record was successfully delete')
    return redirect(url_for('recommend'))




if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
