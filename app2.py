from flask import Flask, request, jsonify
import pandas as pd
import json
import os

JSON_FOLDER = os.path.join('static', 'data')
app = Flask(__name__)
app.config['JSON_FOLDER'] = JSON_FOLDER
data_folder = app.config['JSON_FOLDER']
file_a = open(JSON_FOLDER+'\\index_color'+'.json')
tran1 = json.load(file_a)

app = Flask(__name__)
test = [{'col': 'b', 'count': 8}, {'col': 'a', 'count': 10}]


@app.route('/')
def index():
    # 藉由網址傳遞參數 http://127.0.0.1:5000/?x=vivian
    x = request.args.get('x')  # html ? 參數:值
    return '<h1>Hello {} </h1>'.format(x)


@app.route('/data')
def data():
    df = pd.DataFrame(test)
    # RESTFUL~~~~~
    # 從URL返回值
    mx = request.args.get('mx')
    mn = request.args.get('mn')
    # http://127.0.0.1:5000/data?mx=10&mn=9
    if mx != None and mx != 'None' and mn != None and mn != 'None':
        df = df[(df.count < int(mx)) & (df.count > int(mn))]

    # in javascript: chart.dataSource.url="/data"
    # 返回json
    return jsonify(df.to_dict(orient='records'))


app.run(debug=True)
