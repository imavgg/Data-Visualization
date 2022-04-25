from sklearn.metrics import classification_report, confusion_matrix
import pickle
import pandas as pd
import statistics
import numpy as np
class output():
    def __init__(self, predict,article ,price,alive,cluster_age_avgconsume, 
            loyaty, age_class, attribute, graphical_rename, color_rename,garment_group_name,avg_consume,Buy_n_year):
        self.predict=predict
        self.article=article
        self.price=price
        self.cluster_age_avgconsume=cluster_age_avgconsume
        self.alive=alive
        self.Buy_n_year=Buy_n_year
        self.loyaty=loyaty
        self.avg_consume=avg_consume
        self.age_class=age_class
        self.attribute=attribute
        self.graphical_rename=graphical_rename
        self.color_rename=color_rename
        self.garment_group_name=garment_group_name

def lgbm():
    with open('Model_2/LGBM.pickle','rb') as fr:
        return pickle.load(fr)
    
def xgboost():
    with open('Model_2/xgboost.pickle','rb') as fr:
        return pickle.load(fr)
    
def RandomForest():
    with open('Model_2/RandomForest.pickle','rb') as fr:
        return pickle.load(fr)

#產出網頁的原始16個article_id
def cus_id(cusid):
    df_demo = pd.read_csv('Model_2/cus12(Org).csv',dtype={'article_id': str})
    prod_id = df_demo[df_demo['customer_id']==cusid]['article_id'].tolist()
    return(prod_id)


# 回傳customer 輸入進表的table
def input(cus,article_list):
    df_demo = pd.read_csv('Model_2/cus12(Org).csv',dtype={'article_id': str})
    feature=['price','cluster_age_avgconsume','alive','Buy_n_year','loyaty','avg_consume','age_class','attribute','graphical_rename','color_rename','garment_group_name']
    df_demo = df_demo[df_demo['customer_id']==cus]
    x_test=pd.DataFrame()
    for i in article_list:
        a=df_demo[df_demo['article_id']==i]
        x_test=x_test.append(a,ignore_index=True) 

    #僅取部分特徵
    x_test = x_test[feature]

    return(x_test)

# 回傳customer 輸入進表的table
def feat2arr(cus,article_list):
    df_demo = pd.read_csv('Model_2/cus12(Org).csv',dtype={'article_id': str})
    allcols=['price','alive','cluster_age_avgconsume', 'loyaty', 'age_class', 'attribute', 'graphical_rename',
    'color_rename','garment_group_name','avg_consume','Buy_n_year']
    # customer buy articles columns    #僅取部分特徵

    df_demo = df_demo[df_demo['customer_id']==cus][allcols]
    
    # print(df_demo)

    x = df_demo.to_dict('index')
    val = x.values()
    key = x.keys()
    # 16*11
    all_art=np.zeros((len(key),11))
    count = 0
    for k,v in x.items():
        # print(k,v,'\n')
        # 1*11
        one_art=np.zeros((1,11)) # for multi-dim
        col=0
        for v_k,v_v in v.items():
            one_art[0,col]=v_v
            col+=1
        # print(one_art)
        all_art[count]=one_art
        count+=1

    # print((all_art).shape)
    # print(all_art)


    return(all_art)


# feat2arr('cus_10',cus_id('cus_10')) 

#廠商點商品後 回傳article_list進去做預測
def predict(cus,article_list):
    x_test = input(cus,article_list)

    # print(x_test)

    # for i in x_test[feature]:
    #     print(i)

    # print( [f] for f in x_test[feature].count()  )


    #模型預測:返回一串 list(1 or 0 )for y_test
    lgbm_pre = lgbm().predict(x_test)
    xgboost_pre = xgboost().predict(x_test)
    RandomForest_pre = RandomForest().predict(x_test)

    #Vote
    vote_list = []
    # 將 list 合併
    for i,j,k in zip(lgbm_pre,xgboost_pre,RandomForest_pre):
        x = [i,j,k]
        # 取三個MODEL返回值(1,0)得眾數
        mode = statistics.mode(x)
        vote_list.append(mode)


    # buylist =predict=1 的 article_id

    buy_list=[]
    for i in range(len(vote_list)):
        if vote_list[i]==1:
            buy_list.append(article_list[i])


    return buy_list



###########################################################

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
# feature=['price','cluster_age_avgconsume','alive','Buy_n_year','loyaty','avg_consume','age_class','attribute','graphical_rename','color_rename','garment_group_name']

# predict('cus_10',cus_id('cus_10'))