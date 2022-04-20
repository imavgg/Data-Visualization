#讀出訓練好的模型
def lgbm():
    with open('Model_2/LGBM.pickle','rb') as fr:
        return pickle.load(fr)
    
def xgboost():
    with open('Model_2/xgboost.pickle','rb') as fr:
        return pickle.load(fr)
    
def RandomForest():
    with open('Model_2/RandomForest.pickle','rb') as fr:
        return pickle.load(fr)

#跑全部測試資料集預測
def predict(x,y,z):
    #讀測試資料集
    x_test = pd.read_csv('x_test.csv')
    y_test = pd.read_csv('y_test.csv')

    #模型預測
    lgbm_pre=x.predict(x_test)
    xgboost_pre=y.predict(x_test)
    RandomForest_pre=z.predict(x_test)
    
    #Vote
    vote_list=[]
    for i,j,k in zip(lgbm_pre,xgboost_pre,RandomForest_pre):
        _=[i,j,k]
        mode=statistics.mode(_)
        vote_list.append(mode)
    d=confusion_matrix(y_test,vote_list)
    recall_vote = d[1][1]/d[1].sum()
    accuracy_vote = (d[0][0]+d[1][1])/len(y_test)
    print(f'1對的機率:{recall_vote},整體對的機率:{accuracy_vote}')
    print(d)

#網頁的原始16個article_id
def article_id(cus):
    df_demo = pd.read_csv('Model_2/cus12(Org).csv',dtype={'article_id': str})
    return df_demo[df_demo['customer_id']==cus]['article_id'].tolist()


def predict_product_id(x,y,z,cus):
    #讀測試資料集
    df_demo = pd.read_csv('Model_2/cus12(Org).csv',dtype={'article_id': str})
    feature=['price','cluster_age_avgconsume','alive','Buy_n_year','loyaty','avg_consume','age_class','attribute','graphical_rename','color_rename','garment_group_name']
    x_test = df_demo[df_demo['customer_id']==cus]
    x_output = pd.DataFrame(x_test['article_id'],columns=['article_id'])
    y_test = x_test['Buy']
    x_test = x_test[feature]

    #模型預測
    lgbm_pre=x.predict(x_test)
    xgboost_pre=y.predict(x_test)
    RandomForest_pre=z.predict(x_test)
    
    #Vote
    vote_list=[]
    for i,j,k in zip(lgbm_pre,xgboost_pre,RandomForest_pre):
        _=[i,j,k]
        mode=statistics.mode(_)
        vote_list.append(mode)
    x_output['predict']=vote_list
    return x_output[x_output['predict']==1]['article_id'].values
###########################################################

import pandas as pd
'''
from sklearn.metrics import classification_report, confusion_matrix
import pickle
import statistics

# #1.將已經訓練好的模型讀出
# x=lgbm()
# y=RandomForest()
# z=xgboost()
# #2.跑模型預測
# predict(x,y,z)


#Demo給廠商用的,product接的是客戶會買的商品ID的List
#1.先將已經訓練好的模型讀出
x=lgbm()
y=xgboost()
z=RandomForest()
#2.跑模型進行預測    cus = 客戶,從1~12，用str寫,如"cus_1~12"
cus = 'cus_10'
product = predict_product_id(x,y,z,cus)
print(product)
'''
def cus_id(cusid):
    cus = cusid
    #產出網頁的原始16個article_id
    prod_id = article_id(cus)
    return(prod_id)