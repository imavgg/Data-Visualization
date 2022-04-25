import numpy as np
import pandas as pd
from Model_2 import for_test as ft 

# original:
# ['price', 'cluster_age_avgconsume', 'alive', 'Buy_n_year', 'loyaty', 'avg_consume', 'age_class', 'attribute', 
# 'graphical_rename', 'color_rename', 'garment_group_name']

# DB: 11
allcols=['price','alive','cluster_age_avgconsume',
 'loyaty', 'age_class', 'attribute', 'graphical_rename',
 'color_rename','garment_group_name','avg_consume','Buy_n_year']

# method 1 : by keys values

def to_db(x):
    # DB:9
    cols=['alive','cluster_age_avgconsume', 'loyaty', 
    'age_class', 'attribute', 'graphical_rename',
    'color_rename','garment_group_name','Buy_n_year']
    
    times=x.shape[0] # read items 16
    
    # 找平均數: 一行行讀
    sum=0
    for i in range(times):
        sum+= x[i][0]
    # avg price
    # print('----------------------------A---------')

    # 找眾數:
    ## 找不同values
    def find_diff_names(x,j):
        # ex: x=[a,b,c,c,d,e]
        diff_names=[]
        for i in range(times):
            # 如果不等於初始值 也還沒add進diff names
            # if not x[i]['keys'] in or not x[i]['key']==x[0]['keys']
            if not x[i][j] in diff_names or not x[i][j]==x[0][j]:
                diff_names.append(x[i][j])
        # print(diff_names)
        return(diff_names)

    ## 找重複的不同values數量
    def group_list(diff_names):
        diff_counts=[0]*len(diff_names)
        diff= zip(diff_names,diff_counts) #easy to see

        # read every articles
        for i in range(times):
            # read name in diff_names
            for j in range(len(diff_names)):
                if (x[i][col]==diff_names[j]):
                    diff_counts[j]+=1
                else:pass

        # print(list(diff))
        return(diff_counts)

    def max_value(diff_names,diff_counts):
        max = diff_counts[0]
        max_num =0
        for j in range(len(diff_counts)):
            if diff_counts[j]>max:
                max = diff_counts[j]
                max_num = j
            else:pass
        # print(diff_names[max_num])
        return(diff_names[max_num])

    ## 找出回傳顧客購物車選取最多的值
    most_list=[]
    for col in range(len(cols)):
        diff_names = find_diff_names(x,col)
        diff_counts=group_list(diff_names)
        max_index = max_value(diff_names,diff_counts)
        most_list.append(int(max_index))

    # print(most_list)
    # print('----------------------------RETURN---------')
    
    commons=np.array([0]*len(allcols),dtype=float)
    commons[0]=round(sum/times,3) #price
    commons[1:8]=most_list[0:7]
    commons[9]=(round(x[0,9],3)) #avg_consume
    commons[10]=most_list[8]

    print(commons)
    return(commons)


# x = ft.feat2arr('cus_10',ft.cus_id('cus_10')) 
# y = to_db(x)
# print(y)





    
        


    