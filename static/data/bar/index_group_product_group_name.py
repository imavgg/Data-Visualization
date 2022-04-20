# -*- coding: utf-8 -*-
"""index_group_product_group_name

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1o0tcx5T5BS05f2-yz44sFJNoJ2E44dgM
"""

#from google.colab import files
#uploaded =files.upload()

#輸入資料
import pandas as pd
import numpy as np
from pandas import DataFrame


data1 = pd.read_csv('/Users/Min-Ni/Desktop/articles.csv')
data1.head()
data1.columns

newdata1=data1.groupby(['index_group_name','product_group_name']).size()
newdata1.to_frame()
print(newdata1)
#iterows
listcomb1=[]
newdata1_num=len(newdata1)
#輸出子項目總共數量（子項目＆數字）
for i in newdata1:
  listcomb1.append(i)
print(listcomb1)

#講newdata1轉成字典，再拆開字典key值
#('Baby/Children', 'Bright') 不滿意
dickey=newdata1.to_dict()
def getList(dict):
    return dict.keys()
col1=[]
col2=[]
for i in range(newdata1_num):
    keycomb=getList(dickey)
    keycomb=list(keycomb)
    one,two=keycomb[i]
    col1.append(one)
    col2.append(two)
print(col1)
print(col2)
final=[]

columns_final=['index_group_name','product_group_name']
index_group_name=col1
product_group_name=col2

#記得listcomb1要除以總數
#計算限定下子項數目總和


#再填回counts
d = {'index_group_name': index_group_name, 'product_group_name': product_group_name,'counts':listcomb1}
print(d)
d=pd.DataFrame(d)
print(d)

rowd=pd.crosstab(index=d['index_group_name'],columns=d['product_group_name'],values=d['counts'],aggfunc='sum',normalize='index')
print(rowd)

rowd.shape

js = rowd.to_json(orient = 'index')
print(js)
js1 = rowd.to_json(orient = 'columns')
print(js1)
js2 = rowd.to_json(orient = 'split')
print(js2)
js3 = rowd.to_json(orient = 'table')
print(js3)

#第一個[]是類別
#第二個[]是顏色

aa=list(set(index_group_name))
bb=list(set(product_group_name))
print(aa)
print(bb)
index=[]
row_1=rowd.iloc[0]
row_2=rowd.iloc[0]
row_3=rowd.iloc[0]
for i in range(len(aa)):
  for m in range(len(bb)):
    bb[m]
    g=(bb[m],rowd.iloc[i][m])
    index.append(g)
    print(index[-1])
