# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 08:36:05 2019

@author: fg010
"""
#%%
import json
import pandas as pd
import numpy as np
import os

#%%
"""该路径的所有json读取 时间较长"""
dirs = 'D:\data\掌厨\菜谱'
CommentList = []
DishesCommensense = []
DishesMaterial = []
DishesSuitable = []
DishesView = []
RecommendLike = []
for parent, dirnames, filenames in os.walk(dirs):
    for filename in filenames:
#            print("parent is: " + parent)
            # print("filename is: " + filename)
            
        with open(os.path.join(parent,'CommentList.json'), 'r',encoding='utf-8') as f:
            data = json.load(f)
            CommentList += [data]
            
        with open(os.path.join(parent,'DishesCommensense.json'), 'r',encoding='utf-8') as f:
            data1 = json.load(f)
            DishesCommensense += [data1]
            
        with open(os.path.join(parent,'DishesMaterial.json'), 'r',encoding='utf-8') as f:
            data2 = json.load(f)
            DishesMaterial += [data2]
            
        with open(os.path.join(parent,'DishesSuitable.json'), 'r',encoding='utf-8') as f:
            data3 = json.load(f)
            DishesSuitable += [data3]
            
        with open(os.path.join(parent,'DishesView.json'), 'r',encoding='utf-8') as f:
            data4 = json.load(f)
            DishesView += [data4]
            
        with open(os.path.join(parent,'RecommendLike.json'), 'r',encoding='utf-8') as f:
            data5 = json.load(f)
            RecommendLike += [data5]
        # print(os.path.join(parent, filename))  # 输出rootdir路径下所有文件（包含子文件）信息
        # print(os.path.join(parent,'CommentList.json'))  # 输出rootdir路径下所有文件（包含子文件）信息

#%%
"""data 1 关键食材介绍 提示"""
nutrition_analysis = []
production_direction = []
for i in DishesCommensense:
    nutrition_analysis += [i['data']['nutrition_analysis']]
    production_direction += [i['data']['production_direction']]
#%%
"""data2 食材"""
material = []
for i in DishesMaterial:
    # print(i['data']['material'])
    
    material_s = ''
    for j in i['data']['material']:
        material_s += str(j['material_name'])
        material_s += '：'
        material_s += str(j['material_weight'])
        material_s += ';\n'
    material += [material_s]
#%%
"""data4 菜的详细资料"""
dashes_name = []
hard_level = []
taste = []
cooke_time = []
material_desc = []
share_amount = []
dishes_title = []
agreement_amount = []

tags = []
tags1 = []
tags2 = []
tags3 = []
tags4 = []
step = []

for i in DishesView:
    # print(i['data']['tags_info'])
    # for j in range(len(i['data']['tags_info'])):
        # print(i['data']['tags_info'][j]['text'])
        
    dashes_name += [i['data']['dashes_name']]
    hard_level += [i['data']['hard_level']]
    taste += [i['data']['taste']]
    cooke_time += [i['data']['cooke_time']]
    material_desc += [i['data']['material_desc']]
    share_amount += [i['data']['share_amount']]
    dishes_title += [i['data']['dishes_title']]
    agreement_amount += [i['data']['agreement_amount']]
    
    try: 
        try:
            tags += [i['data']['tags_info'][0]['text']]
        except:
            tags += [np.nan]
        try:
            tags1 += [i['data']['tags_info'][1]['text']]
        except:
            tags1 += [np.nan]
        try:
            tags2 += [i['data']['tags_info'][2]['text']]
        except:
            tags2 += [np.nan]
        try:
            tags3 += [i['data']['tags_info'][3]['text']]
        except:
            tags3 += [np.nan]
        try:
            tags4 += [i['data']['tags_info'][4]['text']]
        except:
            tags4 += [np.nan]
    except:
        continue
    
    step_all =''
    for j in range(len(i['data']['step'])):
        # print(i['data']['step'][j])
        
        step_all += (str(i['data']['step'][j]['dishes_step_order']) + '.')
        step_all += str(i['data']['step'][j]['dishes_step_desc'])
    step += [step_all]

#%%
"""data5 相关推荐菜"""
RecommendLike_content = []
RecommendLike_description = []
RecommendLike_title = []

for i in range(5):
    vars()['content'+str(i)] = []
    vars()['description'+str(i)] = []
    vars()['title'+str(i)] = []
    
for i in range(len(RecommendLike)):
    for j in range(5):
        try:
            vars()['content'+str(j)] += [RecommendLike[i]['data']['data'][j]['content']]
        except:
            vars()['content'+str(j)] += [np.nan]
        try:
            vars()['description'+str(j)] += [RecommendLike[i]['data']['data'][j]['description']]
        except:
            vars()['description'+str(j)] += [np.nan]
        try:
            vars()['title'+str(j)] += [RecommendLike[i]['data']['data'][j]['title']]
        except:
            vars()['title'+str(j)] += [np.nan]
#%%
df = pd.DataFrame()
df['名称'] = dashes_name
df['难度'] = hard_level
df['味道'] = taste
df['时间'] = cooke_time
df['简介'] = material_desc
df['推荐指数'] = share_amount
df['介绍'] = dishes_title
df['同意指数'] = agreement_amount
df['标签'] = tags
df['标签1'] = tags1
df['标签2'] = tags2
df['标签3'] = tags3
df['标签4'] = tags4
df['步骤'] = step
df['食材'] = material
df['关键食材介绍'] = nutrition_analysis
df['提示'] = production_direction

for j in range(5):
    df['相关菜介绍'+str(j)] = vars()['content'+str(j)]
    df['相关菜简介'+str(j)] = vars()['description'+str(j)]
    df['相关菜'+str(j)] = vars()['title'+str(j)]

df = df.drop_duplicates(subset='简介', keep='first', inplace=False) #去重

#%%
"""制作三元组df"""
df2 = pd.DataFrame()
df2['entity'] = []
df2['relations'] = []
df2['value'] = []
column_names = df.columns.values

import re
cop = re.compile("[^\u4e00-\u9fa5]") #仅保留中文

for i in column_names:
    print(i)
    df3 = pd.DataFrame()
    if i != '名称':
        df3['entity'] = df[df[i].notnull()]['名称']
        df3['value'] = df[df[i].notnull()][i]
        
        relation = cop.sub('', i) #仅保留中文关系
        
        df3['relations'] =  [relation for j in range(len(df3['entity']))]     
    df2 = df2.append(df3, ignore_index=True)
    
df2 = df2.drop_duplicates(subset=['entity','value','relations'], keep='first', inplace=False) #去重
df2.reset_index(drop=True, inplace=True) #index 重置
#%%
"""构造ID"""
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
le.fit(df2['entity'])
entity_id = le.transform(df2['entity'])
entity_id = entity_id

# col_name = df2.columns.tolist()
# df2.insert(col_name.index('entity'), 'entity_id:ID', entity_id)

df4 = pd.DataFrame()
df4['entity_id:ID'] = entity_id
df4['entity'] = df2['entity']
df4[':LABEL'] = ['Name' for i in range(len(df2['entity']))]


le1 = LabelEncoder()
le1.fit(df2['value'])
value_id = le1.transform(df2['value'])
value_id = value_id + 1000000

df5 = pd.DataFrame()
df5['value_id:ID'] =  value_id
df5['value'] = df2['value']
df5[':LABEL'] = df2['relations']


df6 = pd.DataFrame()
df6[':START_ID'] = entity_id
df6['role'] = df2['entity']
df6[':END_ID'] =  value_id
df6[':TYPE'] = df2['relations']

#%%
"""导出csv文件"""
df4.to_csv('movies.csv',encoding = 'utf-8',index = False)
df5.to_csv('actors.csv',encoding = 'utf-8',index = False)
df6.to_csv('roles.csv',encoding = 'utf-8',index = False)
#%%
"""对比官方实例"""
df4 = pd.DataFrame()
df5 = pd.DataFrame()
df6 = pd.DataFrame()

df4['movieId:ID'] = ['tt0133093','tt0234215','tt0242653']
df4['title'] = ["The Matrix","The Matrix Reloaded","The Matrix Revolutions"]
df4['year:int'] = [1999,2003,2003]
df4[':LABEL'] = ['Movie','Movie;Sequel','Movie;Sequel']

df5['personId:ID'] = ['keanu','laurenc','carrieanne']
df5['name'] = ["Keanu Reeves","Laurence Fishburne","Carrie-Anne Moss"]
df5[':LABEL'] = ['Actor','Actor','Actor']

df6[':START_ID'] = ['keanu','keanu','keanu','laurenc','laurenc','laurenc','carrieanne','carrieanne','carrieanne']
df6['role'] = ['Neo','Neo','Neo','Morpheus','Morpheus','Morpheus','Trinity','Trinity','Trinity']
df6[':END_ID'] = ['tt0133093','tt0234215','tt0242653','tt0133093','tt0234215','tt0242653','tt0133093','tt0234215','tt0242653']
df6[':TYPE'] = ['ACTED_IN','ACTED_IN','ACTED_IN','ACTED_IN','ACTED_IN','ACTED_IN','ACTED_IN','ACTED_IN','ACTED_IN']

"""
  movieId:ID                   title  year:int        :LABEL
0  tt0133093              The Matrix      1999         Movie
1  tt0234215     The Matrix Reloaded      2003  Movie;Sequel
2  tt0242653  The Matrix Revolutions      2003  Movie;Sequel

  personId:ID                name :LABEL
0       keanu        Keanu Reeves  Actor
1     laurenc  Laurence Fishburne  Actor
2  carrieanne    Carrie-Anne Moss  Actor


    :START_ID      role    :END_ID     :TYPE
0       keanu       Neo  tt0133093  ACTED_IN
1       keanu       Neo  tt0234215  ACTED_IN
2       keanu       Neo  tt0242653  ACTED_IN
3     laurenc  Morpheus  tt0133093  ACTED_IN
4     laurenc  Morpheus  tt0234215  ACTED_IN
5     laurenc  Morpheus  tt0242653  ACTED_IN
6  carrieanne   Trinity  tt0133093  ACTED_IN
7  carrieanne   Trinity  tt0234215  ACTED_IN
8  carrieanne   Trinity  tt0242653  ACTED_IN


        entity_id:ID   entity :LABEL
0              10872    西式凤尾虾   Name
1               2106  奥尔良风味披萨   Name
2              13958   黄桃培根披萨   Name
3               5395   火腿鲜菇披萨   Name
4              12125  金葱鲍鱼粒炒饭   Name
             ...      ...    ...
439489          7265  素食口袋三明治   Name
439490          1575  吐司水果三明治   Name
439491         12817  香烤奶酪三明治   Name
439492          3621  杂粮阳光三明治   Name
439493          3446    早餐三明治   Name
 
        value_id:ID     value :LABEL
0           1017630        一般     难度
1           1017630        一般     难度
2           1017630        一般     难度
3           1017630        一般     难度
4           1017630        一般     难度
            ...       ...    ...
439489      1023536  决明子消脂瘦身汤    相关菜
439490      1078526  虾仁牛油果三明治    相关菜
439491      1034322  家常五香粉蒸肉.    相关菜
439492      1041231     早餐三明治    相关菜
439493      1041231     早餐三明治    相关菜

        :START_ID     role  :END_ID :TYPE
0           10872    西式凤尾虾  1017630    难度
1            2106  奥尔良风味披萨  1017630    难度
2           13958   黄桃培根披萨  1017630    难度
3            5395   火腿鲜菇披萨  1017630    难度
4           12125  金葱鲍鱼粒炒饭  1017630    难度
          ...      ...      ...   ...
439489       7265  素食口袋三明治  1023536   相关菜
439490       1575  吐司水果三明治  1078526   相关菜
439491      12817  香烤奶酪三明治  1034322   相关菜
439492       3621  杂粮阳光三明治  1041231   相关菜
439493       3446    早餐三明治  1041231   相关菜



"""
#%%
"""下面仅供 build_medicalgraph.py 使用，生成json文件所用"""
df.reset_index(drop=True, inplace=True)
data_list = []
for i in range(14395):
    dish_data = {}
    try:
        dish_data['名称'] = df['名称'][i]
        dish_data['难度'] = df['难度'][i]
        dish_data['味道'] = df['味道'][i]
        dish_data['时间'] = df['时间'][i]
        dish_data['简介'] = df['简介'][i]
        dish_data['推荐指数'] = df['推荐指数'][i]
        dish_data['介绍'] = df['介绍'][i]
        dish_data['同意指数'] = df['同意指数'][i]
        clean_tag = [df['标签'][i],df['标签1'][i],df['标签2'][i],df['标签3'][i],df['标签4'][i]]
        clean_tag = [x for x in clean_tag if str(x) != 'nan']
        dish_data['标签'] = clean_tag
        # dish_data['标签'] = df['标签'][i]
        # dish_data['标签1'] = df['标签1'][i]
        # dish_data['标签2'] = df['标签2'][i]
        # dish_data['标签3'] = df['标签3'][i]
        # dish_data['标签4'] = df['标签4'][i]
        dish_data['步骤'] = df['步骤'][i]
        dish_data['食材'] = df['食材'][i]
        dish_data['关键食材介绍'] = df['关键食材介绍'][i]
        dish_data['提示'] = df['提示'][i]
        
        data_list += [dish_data]
    except:
        print(df['名称'][i])

# data_list = list(set(data_list))
for item in data_list:
    try:
        with open('dish_data3.json', 'a+', encoding='utf-8') as f:
            line = json.dumps(item, ensure_ascii=False)
            f.write(line+'\n')
    except:
        print(item)