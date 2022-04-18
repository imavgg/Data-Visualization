import numpy as np
import pandas as pd
import random
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score,confusion_matrix
import dataset
from sklearn.utils import shuffle

import pickle
import pandas as pd
labelencoder = LabelEncoder()


def encode(a,b,c,d,e,f,g,h,i,j):


    #載入資料
    df=pd.read_csv('Model_1/0416.csv')
    df=shuffle(df)

    df=df.drop('department_name',axis=1) #沒刪乾淨 之後確定
    df=df.drop('FN',axis=1)
    df=df.drop('club_member_status',axis=1)
    df=df.drop('Active',axis=1)
    df=df.drop('fashion_news_frequency',axis=1)


    X=pd.DataFrame({'sales_channel_id':[a],
                    'product_group_name':[b],
                    'graphical_appearance_name':[c],
                    'colour_group_name':[d],
                    'section_name':[e],
                    'garment_group_name':[f],
                    'Year':[g],
                    'season':[h],
                    'pricelabel':[i],
                    'salelabel':[j],
                    })

    #加入進大表最後一筆
    df=df.append(X,ignore_index=True)


    #改類型再做LABEL
    df['sales_channel_id']=df['sales_channel_id'].astype('str')
    df['product_group_name']=df['product_group_name'].astype('str')
    df['graphical_appearance_name']=df['graphical_appearance_name'].astype('str')
    df['colour_group_name']=df['colour_group_name'].astype('str')
    df['section_name']=df['section_name'].astype('str')
    df['garment_group_name']=df['garment_group_name'].astype('str')

    df['Year']=df['Year'].astype('str')
    df['season']=df['season'].astype('str')
    df['pricelabel']=df['pricelabel'].astype('str')
    df['salelabel']=df['salelabel'].astype('str')


    df['product_group_name']= labelencoder.fit_transform(df['product_group_name'])
    df['graphical_appearance_name']= labelencoder.fit_transform(df['graphical_appearance_name'])
    df['colour_group_name']= labelencoder.fit_transform(df['colour_group_name'])
    df['section_name']= labelencoder.fit_transform(df['section_name'])
    df['garment_group_name']= labelencoder.fit_transform(df['garment_group_name'])
    #以下實驗
    df['Year']= labelencoder.fit_transform(df['Year'])
    df['pricelabel']= labelencoder.fit_transform(df['pricelabel'])
    df['season']= labelencoder.fit_transform(df['season'])
    df['salelabel']= labelencoder.fit_transform(df['salelabel'])

    TestX=df.tail(1)
    #要移除article_id才是特徵
    TestX=TestX.drop('article_id',axis=1)
    return(TestX)

def predict(TestX):
    model = pickle.load(open('Model_1/MODEL_x2article.pkl','rb'))

    prediction = model.predict(TestX)

    return(prediction)


















