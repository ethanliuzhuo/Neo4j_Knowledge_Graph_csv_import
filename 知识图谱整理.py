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
import re
import jieba
import copy
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
df['介绍'] = material_desc
df['推荐指数'] = share_amount
df['描述'] = dishes_title
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

# for j in range(5):

    # df['相关菜'+str(j)] = vars()['title'+str(j)]
    # df['相关菜介绍'+str(j)] = vars()['content'+str(j)]
    # df['相关菜简介'+str(j)] = vars()['description'+str(j)]

df = df.drop_duplicates(subset='介绍', keep='first', inplace=False) #去重

df_txt1 = copy.deepcopy(df)
#%%
"""制作三元组df"""
df2 = pd.DataFrame()
df2['entity'] = []
df2['relations'] = []
df2['value'] = []
column_names = df.columns.values

import re
cop = re.compile("[^\u4e00-\u9fa5]") #仅保留中文

# pass_list = []

for i in column_names:
    print(i)
    df3 = pd.DataFrame()
    pass_ = ''
    if i != '名称':
        df3['entity'] = df[df[i].notnull()]['名称']
        df3['value'] = df[df[i].notnull()][i]
        
        relation = cop.sub('', i) #仅保留中文关系
        
        df3['relations'] =  [relation for j in range(len(df3['entity']))]  
        
        df3= df3.drop_duplicates(subset=['entity','value','relations'], keep='first', inplace=False) #去重

    df2 = df2.append(df3, ignore_index=True)
    
df2 = df2.drop_duplicates(keep='first', inplace=False) #去重
df2.reset_index(drop=True, inplace=True) #index 重置

dataframe1 = copy.deepcopy(df2)
#%%
"""测试用"""
count = 0
for i in df2['entity']:
    
    if i == '咕噜肉':
        print(df2['entity'][count],'  ', df2['relations'][count],'  ',df2['value'][count][:5])
        
    count += 1
#%%
"""构造ID"""
# from sklearn.preprocessing import LabelEncoder
# le = LabelEncoder()
# le.fit(df2['entity'])
# entity_id = le.transform(df2['entity'])
# entity_id = entity_id

# df4 = pd.DataFrame()
# df4['entity_id:ID'] = entity_id
# df4['entity'] = df2['entity']
# df4[':LABEL'] = ['Name' for i in range(len(df2['entity']))]


# le1 = LabelEncoder()
# le1.fit(df2['value'])
# value_id = le1.transform(df2['value'])
# value_id = value_id + 1000000 #确保每一个ID不重复

# df5 = pd.DataFrame()
# df5['value_id:ID'] =  value_id
# df5['value'] = df2['value']
# df5[':LABEL'] = df2['relations']


# df6 = pd.DataFrame()
# df6[':START_ID'] = entity_id
# df6['role'] = df2['relations']
# df6[':END_ID'] =  value_id
# df6[':TYPE'] = df2['relations']

#%%
"""导出csv文件"""
# df4.to_csv('movies1.csv',encoding = 'utf-8',index = False)
# df5.to_csv('actors1.csv',encoding = 'utf-8',index = False)
# df6.to_csv('roles1.csv',encoding = 'utf-8',index = False)
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
# --nodes /home/wkq/neo4j/node.csv  --relationships /home/wkq/neo4j/relathionship.csv --trim-strings true --input-encoding UTF-8 --id-type INTEGER --stacktrace true --bad-tolerance 0 --skip-bad-relationships true --skip-duplicate-nodes false
# neo4j-admin import --nodes=../import/movies.csv --nodes=../import/actors.csv --relationships=../import/roles.csv
# neo4j-admin import --nodes=../import/actors.csv --nodes=../import/movies.csv --relationships=../import/roles.csv
# neo4j-admin import --nodes=../import/movies.csv --nodes=../import/actors.csv --relationships=../import/roles.csv --multiline-fields=True --skip-duplicate-nodes=True

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
        dish_data['描述'] = df['描述'][i]
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
        print(item)#%%
        
"""下面数据针对分类和食材，build_medicalgraph.py 使用的数据仅在上面"""
#%%
"""分类数据整理"""
dirs = 'D:\data\掌厨\分类'
class_1 = []
class_2 = []
all_data = []
for parent, dirnames, filenames in os.walk(dirs):
    for filename in filenames:
        # print("parent is: " + parent)
        class_s = parent.split("\\")
        class_1 += [class_s[-2]]
        class_2 += [class_s[-1]]
        # print("filename is: " + filename)
        with open(os.path.join(parent,filename), 'r',encoding='utf-8') as f:
            data = json.load(f)
            all_data += [data['data']]

# all_data[0].keys()
#%%
title = [] #名称
description = [] #介绍
hard_level = [] 
cooking_time = []
taste = []
content = [] #介绍
tags0 = []
tags1 = []
tags2 = []
tags3 = []
tags4 = []

comment_count = [] #留言数
agreement_amount = [] #同意指数
share_amount = [] #分享指数
Class_1 = [] #类别
Class_2 = [] #

dishes_id = []
for i in range(len(all_data)):
    # print(all_data[i])
    for j in range(int(all_data[i]['count'])):
        # all_data[i]['data'][j]
        Class_1 += [class_1[i]]
        Class_2 += [all_data[i]['page_title']]
        title += [all_data[i]['data'][j]['title']]
        
        description += [all_data[i]['data'][j]['description']]
        hard_level += [all_data[i]['data'][j]['hard_level']] 
        cooking_time += [all_data[i]['data'][j]['cooking_time']]
        dishes_id += [int(all_data[i]['data'][j]['dishes_id'])]
        taste += [all_data[i]['data'][j]['taste']]
        content += [all_data[i]['data'][j]['content']]
        comment_count += [all_data[i]['data'][j]['comment_count']]
        agreement_amount += [all_data[i]['data'][j]['agreement_amount']]
        share_amount += [all_data[i]['data'][j]['share_amount']]
        try:
            tags0 += [all_data[i]['data'][j]['tags_info'][0]['text']]
        except:
            tags0 += [np.nan]
        try:
            tags1 += [all_data[i]['data'][j]['tags_info'][1]['text']]
        except:
            tags1 += [np.nan]
        try:
            tags2 += [all_data[i]['data'][j]['tags_info'][2]['text']]
        except:
            tags2 += [np.nan]
        try:
            tags3 += [all_data[i]['data'][j]['tags_info'][3]['text']]
        except:
            tags3 += [np.nan]
        try:
            tags4 += [all_data[i]['data'][j]['tags_info'][3]['text']]
        except:
            tags4 += [np.nan]
            
df = pd.DataFrame()
df['名称']= title #名称
df['描述 ']=description
df['难度']=hard_level
df['时间']=cooking_time 
df['味道']= taste
df['介绍']=content
df['标签0']=tags0 
df['标签1']=tags1 
df['标签2']=tags2 
df['标签3']=tags3
df['标签4']=tags4 
df['分享指数']=share_amount
df['留言数']=comment_count 
df['同意指数']=agreement_amount 
df['类别1']=Class_1 
df['类别2']=Class_2
# df['标签5']=Class_1
# df['标签6']=Class_2
# df = df.drop_duplicates(subset='名称') #去重

df_txt2 = copy.deepcopy(df)

#%%
"""制作三元组"""
df7 = pd.DataFrame()
df7['entity'] = []
df7['relations'] = []
df7['value'] = []
column_names = df.columns.values

import re
cop = re.compile("[^\u4e00-\u9fa5]") #仅保留中文

# pass_list = []

for i in column_names:
    print(i)
    df3 = pd.DataFrame()
    pass_ = ''
    if i != '名称':
        df3['entity'] = df[df[i].notnull()]['名称']
        df3['value'] = df[df[i].notnull()][i]
        
        relation = cop.sub('', i) #仅保留中文关系
        
        df3['relations'] =  [relation for j in range(len(df3['entity']))]  
        
        # df3= df3.drop_duplicates(subset=['entity','value','relations'], keep='first', inplace=False) #去重

        df7 = df7.append(df3, ignore_index=True)
    
df7 = df7.drop_duplicates(subset=['entity','value','relations'], keep='first', inplace=False) #去重
df7.reset_index(drop=True, inplace=True) #index 重置

dataframe2 = copy.deepcopy(df7)

#%%
"""测试用"""
count = 0
for i in df7['entity']:
    
    if i == '椒麻四季豆':
        print(df7['entity'][count],'  ', df7['relations'][count],'  ',df7['value'][count][:5])
        
    count += 1
    
df7 = df7.append(df7, ignore_index=True)
#%%
"""构造ID"""
# from sklearn.preprocessing import LabelEncoder
# le = LabelEncoder()
# le.fit(df7['entity'])
# entity_id = le.transform(df7['entity'])
# entity_id = entity_id + 2000000 #确保id不唯一，不与菜谱发生冲突

# df4 = pd.DataFrame()
# df4['entity_id:ID'] = entity_id 
# df4['entity'] = df7['entity']
# df4[':LABEL'] = ['Name' for i in range(len(df7['entity']))]

# le1 = LabelEncoder()
# le1.fit(df7['value'])
# value_id = le1.transform(df7['value'])
# value_id = value_id + 3000000 #确保id不唯一，不与菜谱发生冲突

# df5 = pd.DataFrame()
# df5['value_id:ID'] =  value_id
# df5['value'] = df7['value']
# df5[':LABEL'] = df7['relations']


# df6 = pd.DataFrame()
# df6[':START_ID'] = entity_id
# df6['role'] = df7['relations']
# df6[':END_ID'] =  value_id
# df6[':TYPE'] = df7['relations']
#%%
"""导出csv文件"""
df4.to_csv('movies2.csv',encoding = 'utf-8',index = False)
df5.to_csv('actors2.csv',encoding = 'utf-8',index = False)
df6.to_csv('roles2.csv',encoding = 'utf-8',index = False)
#%%
"""食材生成"""

dirs = 'D:\data\掌厨\食材'

number_data = []
shicai_data = []
class_1 = []
# class_ = []
for parent, dirnames, filenames in os.walk(dirs):
    number_data_value = []
    for filename in filenames:
        # print("parent is: " + parent)
        class_s = parent.split("\\")
        
        # class_2 += [class_s[-1]]
        # print("filename is: " + filename)
        
        if filename[:-5] == class_s[-1]:
            with open(os.path.join(parent,filename), 'r',encoding='utf-8') as f:
                data = json.load(f)
            shicai_data += [data]
            class_1 += [class_s[-2]]
        else:
            with open(os.path.join(parent,filename), 'r',encoding='utf-8') as f:
                data = json.load(f)
            number_data_value += [data]
    number_data += [number_data_value]
    

#%%
"""不知道为什么需要导删除两次"""
for i in number_data:
    if i == []:
        number_data.remove(i)
for i in number_data:
    if i == []:
        number_data.remove(i)
#%%
class_1 #大类
class_ = []
material_name = [] #名称
material_name_2 = [] #长名称
content_ = [] #介绍
pick_ = [] #选购要诀
effect_ = [] #功效
applied_ = [] #应用

title = [] #菜名
hard_level = [] #难度
taste = [] #味道
description = [] #描述
content_long = [] #介绍
cooking_time = [] #时间
tag0 = []
tag1 = []
tag2 = []
tag3 = []
tag4 = []



nutrient_component = []#营养成分
effect = []#功效
content = []#介绍
other_name = [] #别名
variety  = [] #品种
save_way = [] #保存方法
pick_way = [] #选购要诀

clean_cut = [] #清洗与刀工
cook_tip = []#烹饪指南
life_idea = [] #生活妙招
for_good_people = [] #适宜人群
for_bad_people = [] #不宜人群

treatment_food = []   #食疗偏方
collocation_good = [] #搭配相宜
collocation_bad = [] #搭配相克


for i in range(len(shicai_data)):
    # for j in range(len(number_data[i][0]['data']['data'])):
    material_name += [ shicai_data[i]['data']['material_name']]
    # print(j)
    # title += [number_data[i][0]['data']['data'][j]['title']]
    content_ += [shicai_data[i]['data']['content']]
    pick_ += [shicai_data[i]['data']['pick']]
    effect_ += [shicai_data[i]['data']['effect']]
    applied_ += [shicai_data[i]['data']['applied']]

for i in range(len(shicai_data)):
    for j in range(len(number_data[i][0]['data']['data'])):
        material_name_2 += [ shicai_data[i]['data']['material_name']]
        # print(j)
        title += [number_data[i][0]['data']['data'][j]['title']]
        hard_level += [number_data[i][0]['data']['data'][j]['hard_level']]
        taste += [number_data[i][0]['data']['data'][j]['taste']]
        description += [number_data[i][0]['data']['data'][j]['description']]
        content_long += [number_data[i][0]['data']['data'][j]['content']]
        cooking_time += [number_data[i][0]['data']['data'][j]['cooking_time']]
        class_ += []
        try:
            tag0 += [number_data[i][0]['data']['data'][j]['tags_info'][0]['text']]
        except:
            tag0 += [np.nan]
        try:
            tag1 += [number_data[i][0]['data']['data'][j]['tags_info'][1]['text']]
        except:
            tag1 += [np.nan]
        try:
            tag2 += [number_data[i][0]['data']['data'][j]['tags_info'][2]['text']]
        except:
            tag2 += [np.nan]
        try:
            tag3 += [number_data[i][0]['data']['data'][j]['tags_info'][3]['text']]
        except:
            tag3 += [np.nan]
        try:
            tag4 += [number_data[i][0]['data']['data'][j]['tags_info'][4]['text']]
        except:
            tag4 += [np.nan]

for i in applied_:
    if '【清洗与刀工】' in i:
        c = i.split('【清洗与刀工】')[1].split('【')[0].strip()
        clean_cut += [c]
    elif '清洗与刀工' in i:
        c = i.split('清洗与刀工')[1].split('【')[0].strip()
        clean_cut += [c]
    elif '【清洗】' in i:
        c = i.split('【清洗】')[1].split('【')[0].strip()
        clean_cut += [c]
    else:
        clean_cut += ['暂未知']
        # print(applied_.index(i))
    
    if '【烹饪指南】' in i:
        c = i.split('【烹饪指南】')[1].split('【')[0].strip()
        cook_tip += [c]
    # elif '清洗与刀工' in i:
    #     c = i.split('清洗与刀工')[1].split('【')[0].strip()
    #     clean_cut += [c]

    else:
        cook_tip += ['暂未知']
        # print(applied_.index(i))
        
    if '【生活妙招】' in i:
        c = i.split('【生活妙招】')[1].split('【')[0].strip()
        life_idea += [c]
    else:
        life_idea += ['暂未知']
        # print(applied_.index(i)) 
        
    if '【适宜人群】' in i:
        c = i.split('【适宜人群】')[1].split('【')[0].strip()
        for_good_people += [c]
    else:
        for_good_people += ['暂未知']
        # print(applied_.index(i))
        
    if '【不宜人群】' in i:
        c = i.split('【不宜人群】')[1].split('【')[0].strip()
        for_bad_people += [c]
    else:
        for_bad_people += ['暂未知']
        # print(applied_.index(i))   
        
    if '【食疗偏方】' in i:
        c = i.split('【食疗偏方】')[1].split('【')[0].strip()
        treatment_food += [c]
    elif '食疗偏方' in i:
        c = i.split('食疗偏方')[1].split('【')[0].strip()
        treatment_food += [c]
    else:
        treatment_food += ['暂未知']
        # print(applied_.index(i))  
        
    if '【搭配宜忌】' in i:
        if '相宜' in i:
            c = i.split('【搭配宜忌】')[1].split('相宜')[1].split('相克')[0].strip()
            collocation_good += [c]
        else:
            collocation_good += ['暂未知']
            
        if '相克' in i and '相宜' in i:    
            d = i.split('【搭配宜忌】')[1].split('相宜')[1].split('相克')[1].strip()
            collocation_bad += [d]
        elif '相克' in i and '相宜' not in i: 
            d = i.split('【搭配宜忌】')[1].split('相克')[1].strip()
            collocation_bad += [d]
        else:
            collocation_bad += ['暂未知']
    # elif '食疗偏方' in i:
    #     c = i.split('食疗偏方')[1].split('【')[0].strip()
    #     collocation_good += [c]
    else:
        collocation_good += ['暂未知']
        collocation_bad += ['暂未知']
        print(applied_.index(i))  

for i in pick_:
    if '【选购要诀】' in i and '【保存方法】' in i:
        c = i.split('【选购要诀】')[1].split('【保存方法】')[0].strip()
        pick_way += [c]
         
    elif '【选购要诀】' in i and '【保存方法】' not in i:
        c = i.split('【选购要诀】')[1].strip()
        pick_way += [c]
    else:
        c = i.split('【保存方法】')[0].strip()
        pick_way += [c]
        
    if '【选购要诀】' in i and '【保存方法】' in i:
        c = i.split('【选购要诀】')[1].split('【保存方法】')[1].strip()
        save_way += [c]
    elif '【选购要诀】' not in i and '【保存方法】' in i:
        c = i.split('【保存方法】')[1].strip()
        save_way += [c]
        
    else:
        save_way += ['暂未知']
        # print(pick_.index(i))

        
for i in effect_:
    try:
        i_split = i.split('【养生功效】')
        effect += [i_split[1].strip()]
        i_split = i_split[0].split('【营养成分】')
        nutrient_component += [i_split[1].strip()]
    except:
        #缺失一个 起酥油
        effect += ['1.起酥油中含有多种维生素，营养价值颇高。其中B族维生素可刺激消化液分泌，促进肠道蠕动，有利于排便。']
        nutrient_component += ['起酥油是指精炼的动、植物油脂、氢化油或上述油脂的混合物，经急冷捏合或不经急冷捏合加工而成的具有可塑性、乳化性等功能特性的固体状或流体状油脂制品']


for i in content_:
    
    if '【' in i:
        
        if i.split('【')[0] == '':
            content += ['介绍暂无，你可以查询其他信息，如别名等']
        else:
            content += [i.split('【')[0].strip()]
    elif '别名' in i:
        content += [i.split('别名')[0].strip()]
    else:
        content += [i]
        # print(content_.index(i))

    if '别名' not in i:
        other_name += [['暂未知']]
    elif ('【别名】' in i) and ('【品种】' in i):
        try:
            c = i.split('【别名】')[1].split('【品种】')[0].strip()
            other_name += [re.split(r'[、。]',c)]
        except:
            print(content_.index(i))
            # print(i)
    elif ('别名' in i) and ('品种' in i):
        try:
            c = i.split('别名')[1].split('品种')[0].strip()
            other_name += [re.split(r'[、。]',c)]
        except:
            print(content_.index(i))
    elif ('【别名】' in i) and ('【品种】' not in i):
        c = i.split('【别名】')[1].split('【品种】')[0].strip()
        other_name += [re.split(r'[、。]',c)]
        
    else:
        print(content_.index(i))

    if '品种'  not in i:
        variety += [['暂未知']]
        
    elif ('【别名】' in i) and ('【品种】' in i):
        c = i.split('【品种】')[1].strip()
        c = c.replace('】', '')
        # c = re.split(r'[\r/\n][/1./2./3./4./5./6./7./8./9./10.]',c)
        # c[0] = c[0].replace('1.', '')
        variety += [[c]]
        # print(content_.index(i))
        # print(i)
    elif ('别名' in i) and ('品种' in i):
        c = i.split('品种')[1].strip()
        c = re.split(r'[\r/\n][/1./2./3./4./5./6./7./8./9./10.]',c)
        c[0] = c[0].replace('1.', '')
        variety += [[c]]
        # print(content_.index(i))
    elif ('【品种】' in i) and ('【别名】' not in i):
        c = i.split('【品种】')[1].strip()
        c = re.split(r'[\r/\n][/1./2./3./4./5./6./7./8./9./10.]',c)
        c[0] = c[0].replace('1.', '')
        variety +=  [[c]]
    elif content_.index(i) == 135:
        variety += [['暂未知']]
        
    else:
        print(content_.index(i))
#%%
"""菜名 - 名称"""
df10 = pd.DataFrame()
df10['名称'] = material_name_2
df10['菜名'] = title #菜名
df10['难度'] = hard_level #难度
df10['味道'] = taste #味道
df10['描述'] = description #描述
df10['介绍'] = content_long #介绍
df10['时间'] = cooking_time #时间
df10['标签0'] = tag0
df10['标签1'] = tag0
df10['标签2'] = tag2
df10['标签3'] = tag3
df10['标签4'] = tag4

df_txt3 = copy.deepcopy(df10)

#%%
"""制作三元组"""
df11 = pd.DataFrame()
df11['entity'] = []
df11['relations'] = []
df11['value'] = []
column_names = df10.columns.values

cop = re.compile("[^\u4e00-\u9fa5]") #仅保留中文

for i in column_names:
    print(i)
    df3 = pd.DataFrame()
    pass_ = ''
    if i != '菜名':
        df3['entity'] = df10[df10[i].notnull()]['菜名']
        df3['value'] = df10[df10[i].notnull()][i]
        
        relation = cop.sub('', i) #仅保留中文关系
        
        if relation == '名称':
            df3['relations'] =  ['类别' for j in range(len(df3['entity']))]  
        else:
            df3['relations'] =  [relation for j in range(len(df3['entity']))]  
        
        df11 = df11.append(df3, ignore_index=True)
        
df3 = pd.DataFrame()
df3['entity'] = df10['名称']
df3['relations'] =  ['推荐菜' for j in range(len(df3['entity']))]  
df3['value'] = df10['菜名']
df11 = df11.append(df3, ignore_index=True)
           
#%%
df12 = pd.DataFrame()
df12['名称']  = material_name #名称
df12['类别']  =class_1 
df12['营养成分']  =nutrient_component  #营养成分
df12['功效']  =effect  #功效
df12['介绍']  =content  #介绍
df12['别名']  =other_name   #别名
df12['品种']  =variety    #品种
df12['保存方法']  =save_way   #保存方法
df12['选购要诀']  =pick_way   #选购要诀
df12['清洗与刀工']  =clean_cut   #清洗与刀工
df12['烹饪指南']  =cook_tip  #烹饪指南
df12['生活妙招']  =life_idea  #生活妙招
df12['适宜人群']  =for_good_people  #适宜人群
df12['不宜人群']  =for_bad_people  #不宜人群
df12['食疗偏方']  =treatment_food     #食疗偏方
df12['搭配相宜']  =collocation_good   #搭配相宜
df12['搭配相克']  =collocation_bad   #搭配相克

df_txt4 = copy.deepcopy(df12)

#%%
# df11 = pd.DataFrame()
# df11['entity'] = []
# df11['relations'] = []
# df11['value'] = []

column_names = df12.columns.values

cop = re.compile("[^\u4e00-\u9fa5]") #仅保留中文

# pass_list = []

for number, i in enumerate(column_names):
    # print(i)
    df3 = pd.DataFrame()
    pass_ = ''
    if i != '名称':
        if isinstance(df12[i][0], list):
            entity = []
            value = []
            relations = []
            for j in df12[i]:
                entity += [df12[df12[i].notnull()]['名称'][number]]
                value += [j]
                relations += [i]
        else:
            df3['entity'] = df12[df12[i].notnull()]['名称']
            df3['value'] = df12[df12[i].notnull()][i]
            
            relation = cop.sub('', i) #仅保留中文关系
            
            df3['relations'] =  [relation for j in range(len(df3['entity']))]  
        
        # df3= df3.drop_duplicates(subset=['entity','value','relations'], keep='first', inplace=False) #去重

        df11 = df11.append(df3, ignore_index=True)
df11 = df11.drop_duplicates( keep='first', inplace=False) #去重
df11.reset_index(drop=True, inplace=True) #index 重置

dataframe3 = copy.deepcopy(df11)

#%%
"""测试用"""
count = 0
for i in df11['entity']:
    if i == '土豆炖排骨':
        print(df11['entity'][count],'  ', df11['relations'][count],'  ',df11['value'][count][:5])
    count += 1
    
count = 0
for i in df11['entity']:
    if i == '苦菊':
        print(df11['entity'][count],'  ', df11['relations'][count],'  ',df11['value'][count][:5])
    count += 1    
    
#%%

dataframe =  dataframe1
dataframe = dataframe.append(dataframe2, ignore_index=True)
dataframe = dataframe.append(dataframe3, ignore_index=True)
#%%
"""构造ID"""
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
le.fit(dataframe['entity'])
entity_id = le.transform(dataframe['entity'])
entity_id = entity_id 

df4 = pd.DataFrame()
df4['entity_id:ID'] = entity_id
df4['entity'] = dataframe['entity']
df4[':LABEL'] = ['Name' for i in range(len(dataframe['entity']))]


le1 = LabelEncoder()
le1.fit(dataframe['value'])
value_id = le1.transform(dataframe['value'])
value_id = value_id + 10000000

df5 = pd.DataFrame()
df5['value_id:ID'] =  value_id
df5['value'] = dataframe['value']
df5[':LABEL'] = dataframe['relations']


df6 = pd.DataFrame()
df6[':START_ID'] = entity_id
df6['role'] = dataframe['relations']
df6[':END_ID'] =  value_id
df6[':TYPE'] = dataframe['relations']
#%%
"""导出csv文件"""
# df4.to_csv('movies3.csv',encoding = 'utf-8',index = False)
# df5.to_csv('actors3.csv',encoding = 'utf-8',index = False)
# df6.to_csv('roles3.csv',encoding = 'utf-8',index = False)
"""导出csv文件"""
df4.to_csv('node1.csv',encoding = 'utf-8',index = False)
df5.to_csv('node2.csv',encoding = 'utf-8',index = False)
df6.to_csv('relations.csv',encoding = 'utf-8',index = False)

#%%
cop = re.compile("[^\u4e00-\u9fa5]") #仅保留中文

for i in set(dataframe['relations']):
    # filename = 'dict/'+ str(i) +'.txt'
    vars()[str('f_' +i)]= open('dict/'+ str(i)+ '.txt', 'w+',encoding="utf-8")
    vars()[str(i)]=[]
    vars()[str(i)+'_list']=[]

for i in range(len(dataframe)):
    vars()[dataframe['relations'][i]] += [dataframe['value'][i]]
#%%
save_list = []

for i in range(len(dataframe)):
    if dataframe['relations'][i] == '标签':
        save_list += [dataframe['value'][i]]
        
#%%
for i in 保存方法:
    
    a =  re.split(r'[\r/\n]',i)
    for j in a:
        if "." in j:
            save_list += [j[2:7]]    
list(set(save_list))
#%%
shicai = 食材
for i in shicai:
    
    print(i.split('\n')[0][:-1])

#%%
save_way = 保存方法
q = 0
for value_number, i in enumerate(save_way):
    for number in range(10):
        number_value = str(number) + '.'
        # if i.split(number_value)[0] == '':
        try:
            # print(value_number)
            print(i.split(number_value)[1].split('：')[0].split('\r\n')[0])
            print(i.split(number_value)[1].split('：')[1])
            q += 1
        except:
            pass
            
            
        
        

#%%
# for i in set(dataframe['relations']):
    
#     for sentence in i:
#         seg_list = jieba.cut(sentence)
#         for j in seg_list:
#             j = cop.sub('', j) #仅保留中文关系
#             vars()[str(i)+'_list'] += [j]
#     #%%

# # cut_list = [营养成分,选购要诀,提示,适宜人群]
# cut_list = [选购要诀]
# for cut_value in cut_list:
#     vars()[str(cut_value)+'_list'] = []
#     for sentence in cut_value:
#         seg_list = jieba.cut(sentence)
#         # seg_list = jieba.cut_for_search(sentence)  # 搜索引擎模式
#         for i in seg_list:
#             i = cop.sub('', i) #仅保留中文关系
#             vars()[str(cut_value)+'_list'] += [i]
#         # print(" ".join(seg_list)) # 精确模式
#     vars()[str(cut_value)+'_list'] = list(set(vars()[str(cut_value)+'_list']))
#     print(len(vars()[str(cut_value)+'_list']))
# #%%
# vars()[str(cut_value)] = list(set(vars()[str(cut_value)+'_list']))
# vars()[str('f_' +cut_value)].write('\n'.join(vars()[cut_value]))
# vars()[str('f_' +cut_value)].close()
    #%%
for i in set(dataframe['relations']):
    vars()[str(i)] = list(set(vars()[str(i)]))
    vars()[str('f_' +i)].write('\n'.join(vars()[i]))
    vars()[str('f_' +i)].close()
    
            # f_production_direction= open('production_direction.txt', 'w+')
        
#         f_dashes_name.write('\n'.join(list(Dashes_name)))
#         f_hard_level.write('\n'.join(list(Hard_level)))
#         f_taste.write('\n'.join(list(Taste)))
#         f_cooke_time.write('\n'.join(list(Cooke_time)))
#         f_material_desc.write('\n'.join(list(Material_desc)))
#         f_share_amount.write('\n'.join(list(Share_amount)))
#         f_dishes_title.write('\n'.join(list(Dishes_title)))
#         f_agreement_amount.write('\n'.join(list(Agreement_amount)))
#         f_tags.write('\n'.join(list(Tags)))
#         f_step.write('\n'.join(list(Step)))
#         f_material.write('\n'.join(list(Material)))
#         f_nutrition_analysis.write('\n'.join(list(Nutrition_analysis)))
#         f_production_direction.write('\n'.join(list(Production_direction)))


#         f_dashes_name.close()
