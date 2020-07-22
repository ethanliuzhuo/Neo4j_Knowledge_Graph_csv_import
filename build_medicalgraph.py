#!/usr/bin/env python3
# coding: utf-8
# File: MedicalGraph.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-3

import os
import json
from py2neo import Graph,Node

class MedicalGraph:
    def __init__(self):
        cur_dir = '\\'.join(os.path.abspath(__file__).split('\\')[:-1])   # 获取当前绝对路径的上层目录 linux中应用'/'split和join
        self.data_path = os.path.join(cur_dir, 'dish_data3.json')   # 获取json文件路径
        self.g = Graph(
            host="localhost",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="admin")

    '''读取文件'''
    def read_nodes(self):
        
        """共 18 类节点"""
        dashes_name =[]   #名称
        hard_level  =[]  #难度
        taste     =[]    #味道
        cooke_time  =[]  #时间
        material_desc  =[]#简介
        share_amount=[]#推荐指数
        dishes_title=[]#介绍
        agreement_amount=[]#同意指数
        tags=[]#标签
        # tags1=[]#标签1
        # tags2=[]#标签2
        # tags3=[]#标签3
        # tags4=[]#标签4
        step=[]#步骤
        material=[]#食材
        nutrition_analysis=[]#关键食材介绍
        production_direction=[]#提示
        all_infos = []
        
        """构建节点实体关系16共类"""
        rels_hard_level = [] #菜名 - 难度关系
        rels_taste=[]    #菜名 - 味道关系
        rels_cooke_time  =[]  #菜名 - 时间关系
        rels_material_desc  =[]#菜名 - 简介关系
        rels_share_amount=[]#菜名 - 推荐指数关系
        rels_dishes_title=[]#菜名 - 介绍关系
        rels_agreement_amount=[]#菜名 - 同意指数关系
        rels_tags=[]#菜名 - 标签关系
        # rels_tags1=[]#菜名 - 标签1关系
        # rels_tags2=[]#菜名 - 标签2关系
        # rels_tags3=[]#菜名 - 标签3关系
        # rels_tags4=[]#菜名 - 标签4关系
        rels_step=[]#菜名 - 步骤关系
        rels_material=[]#菜名 - 食材关系
        rels_nutrition_analysis=[]#菜名 - 关键食材介绍关系
        rels_production_direction=[]#菜名 - 提示关系
        


        count = 0
        for data in open(self.data_path,encoding='utf-8'):   # 逐行读取
        # for data in open('dish_data2.json',encoding='utf-8'):   # 逐行读取

            disease_dict = {}
            count += 1
            print('read_nodes: ',count)
            data_json = json.loads(data)
            
            #菜名
            name_dishes = data_json['名称']
            disease_dict['name'] = name_dishes
            dashes_name += [name_dishes]
            
            # disease = data_json['name']
            # disease_dict['name'] = disease
            # diseases.append(disease)
            
            disease_dict['hard_level'] = ''
            disease_dict['taste'] = ''
            disease_dict['cooke_time'] = ''
            disease_dict['material_desc'] = ''
            disease_dict['share_amount'] = ''
            disease_dict['dishes_title'] = ''
            disease_dict['agreement_amount'] = ''
            disease_dict['tags'] = ''
            # disease_dict['tags1'] = ''
            # disease_dict['tags2'] = ''
            # disease_dict['tags3'] = ''
            # disease_dict['tags4'] = ''
            disease_dict['step'] = ''
            disease_dict['material'] = ''
            disease_dict['nutrition_analysis'] = ''
            disease_dict['production_direction'] = ''

            
            if '标签' in data_json:
                tags += data_json['标签']
                
                for tag in data_json['标签']:
                    rels_tags.append([name_dishes,tag])
                disease_dict['tags'] =  data_json['标签']
                
            if '难度' in data_json:
                hard_level += [data_json['难度']]
                disease_dict['hard_level'] = data_json['难度']
                rels_hard_level.append([name_dishes, data_json['难度']])
                
            if '味道' in data_json:
                taste += [data_json['味道']]
                disease_dict['taste'] = data_json['味道']
                rels_taste.append([name_dishes, data_json['味道']])
                
            if '时间' in data_json:
                cooke_time += [data_json['时间']]
                disease_dict['cooke_time'] = data_json['时间']
                rels_cooke_time.append([name_dishes, data_json['时间']])       
                
            if '简介' in data_json:
                material_desc += [data_json['简介']]
                disease_dict['material_desc'] = data_json['简介']
                rels_material_desc.append([name_dishes, data_json['简介']])
                
            if '推荐指数' in data_json:
                share_amount += [data_json['推荐指数']]
                disease_dict['share_amount'] = data_json['推荐指数']
                rels_share_amount.append([name_dishes, data_json['推荐指数']])
                
            if '介绍' in data_json:
                dishes_title += [data_json['介绍']]
                disease_dict['dishes_title'] = data_json['介绍']
                rels_dishes_title.append([name_dishes, data_json['介绍']])
                
            if '同意指数' in data_json:
                agreement_amount += [data_json['同意指数']]
                disease_dict['agreement_amount'] = data_json['同意指数']
                rels_agreement_amount.append([name_dishes, data_json['同意指数']])
                
            if '步骤' in data_json:
                step += [data_json['步骤']]
                disease_dict['step'] = data_json['步骤']
                rels_step.append([name_dishes, data_json['步骤']])
                
            if '食材' in data_json:
                material += [data_json['食材']]
                disease_dict['material'] = data_json['食材']
                rels_material.append([name_dishes, data_json['食材']])
                
            if '关键食材介绍' in data_json:
                nutrition_analysis += [data_json['关键食材介绍']]
                disease_dict['nutrition_analysis'] = data_json['关键食材介绍']
                rels_nutrition_analysis.append([name_dishes, data_json['关键食材介绍']])
                
            if '提示' in data_json:
                production_direction += [data_json['提示']]
                disease_dict['production_direction'] = data_json['提示']
                rels_production_direction.append([name_dishes, data_json['提示']])
                
         
            all_infos.append(disease_dict)
        tags = [x for x in tags if str(x) != 'nan']
        # return set(drugs), set(foods), set(checks), set(departments), set(producers), set(symptoms), set(diseases), disease_infos,\
        #        rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug,\
        #        rels_symptom, rels_acompany, rels_category
        return   set(dashes_name),set(hard_level),set(taste),set(cooke_time),set(material_desc),set(share_amount),set(dishes_title),\
                 set(agreement_amount),set(tags),set(step),set(material),set(nutrition_analysis),set(production_direction),all_infos,\
                 rels_hard_level, rels_taste,rels_cooke_time,rels_material_desc,rels_share_amount,rels_dishes_title,rels_agreement_amount,\
                 rels_tags,rels_step,rels_material,rels_nutrition_analysis,rels_production_direction

    '''建立节点'''
    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print(label, count, len(nodes))
        return

    '''创建知识图谱中心疾病的节点'''
    # def create_diseases_nodes(self, disease_infos):
    def create_dishes_nodes(self, all_infos):
        count = 0
        for disease_dict in all_infos:
            node = Node("Name", name=disease_dict['name'], hard_level=disease_dict['hard_level'],
                                taste=disease_dict['taste'] ,cooke_time=disease_dict['cooke_time'],
                                material_desc=disease_dict['material_desc'] ,share_amount=disease_dict['share_amount'],
                                dishes_title=disease_dict['dishes_title'] ,agreement_amount=disease_dict['agreement_amount'],
                                tags=disease_dict['tags'] ,step=disease_dict['step'],
                                material=disease_dict['material'] ,nutrition_analysis=disease_dict['nutrition_analysis'],
                                production_direction=disease_dict['production_direction'])

            self.g.create(node)
            count += 1
            print('create_dishes_nodes: ',count)
        return

    '''创建知识图谱实体节点类型schema'''
    # def create_graphnodes(self):
    #     Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos,rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug,rels_symptom, rels_acompany, rels_category = self.read_nodes()
    #     self.create_diseases_nodes(disease_infos)
    #     self.create_node('Drug', Drugs)
    #     print(len(Drugs))
    #     self.create_node('Food', Foods)
    #     print(len(Foods))
    #     self.create_node('Check', Checks)
    #     print(len(Checks))
    #     self.create_node('Department', Departments)
    #     print(len(Departments))
    #     self.create_node('Producer', Producers)
    #     print(len(Producers))
    #     self.create_node('Symptom', Symptoms)
    #     return
    def create_graphnodes(self):
        Dashes_name, Hard_level, Taste,Cooke_time, Material_desc, Share_amount, Dishes_title, Agreement_amount,Tags,Step,Material,Nutrition_analysis,Production_direction,all_infos,rels_hard_level, rels_taste,rels_cooke_time,rels_material_desc,rels_share_amount,rels_dishes_title,rels_agreement_amount,rels_tags,rels_step,rels_material,rels_nutrition_analysis,rels_production_direction = self.read_nodes() #25
        
        self.create_dishes_nodes(all_infos)
        
        self.create_node('Dashes_name', Dashes_name)
        print(len(Dashes_name))
        
        self.create_node('Hard_level', Dashes_name)
        print(len(Dashes_name))
        
        self.create_node('Taste', Taste)
        print(len(Taste))
        
        self.create_node('Cooke_time', Cooke_time)
        print(len(Cooke_time))
        
        self.create_node('Material_desc', Material_desc)
        print(len(Material_desc))
        
        self.create_node('Share_amount', Share_amount)
        print(len(Share_amount))
        
        self.create_node('Dishes_title', Dishes_title)
        print(len(Share_amount))
        
        self.create_node('Agreement_amount', Agreement_amount)
        print(len(Agreement_amount))
        
        self.create_node('Tags', Tags)
        print(len(Tags))        
        
        self.create_node('Step', Step)
        print(len(Step))        
        return


    '''创建实体关系边'''
    # def create_graphrels(self):
    #     Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos, rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug,rels_symptom, rels_acompany, rels_category = self.read_nodes()
    #     self.create_relationship('Disease', 'Food', rels_recommandeat, 'recommand_eat', '推荐食谱')
    #     self.create_relationship('Disease', 'Food', rels_noteat, 'no_eat', '忌吃')
    #     self.create_relationship('Disease', 'Food', rels_doeat, 'do_eat', '宜吃')
    #     self.create_relationship('Department', 'Department', rels_department, 'belongs_to', '属于')
    #     self.create_relationship('Disease', 'Drug', rels_commonddrug, 'common_drug', '常用药品')
    #     self.create_relationship('Producer', 'Drug', rels_drug_producer, 'drugs_of', '生产药品')
    #     self.create_relationship('Disease', 'Drug', rels_recommanddrug, 'recommand_drug', '好评药品')
    #     self.create_relationship('Disease', 'Check', rels_check, 'need_check', '诊断检查')
    #     self.create_relationship('Disease', 'Symptom', rels_symptom, 'has_symptom', '症状')
    #     self.create_relationship('Disease', 'Disease', rels_acompany, 'acompany_with', '并发症')
    #     self.create_relationship('Disease', 'Department', rels_category, 'belongs_to', '所属科室')
    def create_graphrels(self):
        Dashes_name, Hard_level, Taste,Cooke_time, Material_desc, Share_amount, Dishes_title, Agreement_amount,Tags,Step,Material,Nutrition_analysis,Production_direction,all_infos,rels_hard_level, rels_taste,rels_cooke_time,rels_material_desc,rels_share_amount,rels_dishes_title,rels_agreement_amount,rels_tags,rels_step,rels_material,rels_nutrition_analysis,rels_production_direction = self.read_nodes() #25


        self.create_relationship('Dashes_name', 'Hard_level', rels_hard_level, 'hard_level', '难度')
        self.create_relationship('Dashes_name', 'Taste', rels_taste, 'taste', '味道')
        self.create_relationship('Dashes_name', 'Cooke_time', rels_cooke_time, 'cooke_time', '时间')
        self.create_relationship('Dashes_name', 'Material_desc', rels_material_desc, 'material_desc', '简介')
        self.create_relationship('Dashes_name', 'Share_amount', rels_share_amount, 'share_amount', '推荐指数')
        self.create_relationship('Dashes_name', 'Dishes_title',rels_dishes_title , 'dishes_title', '介绍')
        self.create_relationship('Dashes_name', 'Agreement_amount', rels_agreement_amount, 'agreement_amount', '同意指数')
        self.create_relationship('Dashes_name', 'Tags',rels_tags , 'tags', '标签')
        self.create_relationship('Dashes_name', 'Step', rels_step, 'step', '步骤')
        self.create_relationship('Dashes_name', 'Material',rels_material , 'material', '食材')
        self.create_relationship('Dashes_name', 'Nutrition_analysis', rels_nutrition_analysis, 'nutrition_analysis', '关键食材介绍')
        self.create_relationship('Dashes_name', 'Production_direction', rels_production_direction, 'production_direction', '提示')


    '''创建实体关联边'''
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        # print(set_edges)
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    # def others(self):
    #     query1 = "match (n) where n.name = '肝硬化' set n.can_eat = '可以喝蜂蜜水，但不具有什么治疗效果。' return n"
    #     query2 = "match (n) where n.name = '乙肝' set n.can_eat = '可以吃海鲜、辛辣食品、肉、巧克力、酸菜、米醋等，适量即可。' return n"
    #     queries = [query1,query2]
    #     for query in queries:
    #         self.g.run(query)

    '''导出数据'''
    # def export_data(self):
    #     Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos, rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug, rels_symptom, rels_acompany, rels_category = self.read_nodes()
    #     f_drug = open('drug.txt', 'w+')
    #     f_food = open('food.txt', 'w+')
    #     f_check = open('check.txt', 'w+')
    #     f_department = open('department.txt', 'w+')
    #     f_producer = open('producer.txt', 'w+')
    #     f_symptom = open('symptoms.txt', 'w+')
    #     f_disease = open('disease.txt', 'w+')

    #     f_drug.write('\n'.join(list(Drugs)))
    #     f_food.write('\n'.join(list(Foods)))
    #     f_check.write('\n'.join(list(Checks)))
    #     f_department.write('\n'.join(list(Departments)))
    #     f_producer.write('\n'.join(list(Producers)))
    #     f_symptom.write('\n'.join(list(Symptoms)))
    #     f_disease.write('\n'.join(list(Diseases)))

    #     f_drug.close()
    #     f_food.close()
    #     f_check.close()
    #     f_department.close()
    #     f_producer.close()
    #     f_symptom.close()
    #     f_disease.close()

        # return
    def export_data(self):
        Dashes_name, Hard_level, Taste,Cooke_time, Material_desc, Share_amount, Dishes_title, Agreement_amount,Tags,Step,Material,Nutrition_analysis,Production_direction,all_infos,rels_hard_level, rels_taste,rels_cooke_time,rels_material_desc,rels_share_amount,rels_dishes_title,rels_agreement_amount,rels_tags,rels_step,rels_material,rels_nutrition_analysis,rels_production_direction = self.read_nodes() #25

        
        f_dashes_name = open('dashes_name.txt', 'w+')
        f_hard_level  = open('hard_level .txt', 'w+')
        f_taste       = open('taste   .txt', 'w+')
        f_cooke_time  = open('cooke_time .txt', 'w+')
        f_material_desc = open('material_desc .txt', 'w+')
        f_share_amount= open('share_amount.txt', 'w+')
        f_dishes_title= open('dishes_title.txt', 'w+')
        f_agreement_amount= open('agreement_amount.txt', 'w+')
        f_tags= open('tags.txt', 'w+')
        f_step= open('step.txt', 'w+')
        f_material= open('f_material.txt', 'w+')
        f_nutrition_analysis= open('nutrition_analysis.txt', 'w+')
        f_production_direction= open('production_direction.txt', 'w+')
        
        f_dashes_name.write('\n'.join(list(Dashes_name)))
        f_hard_level.write('\n'.join(list(Hard_level)))
        f_taste.write('\n'.join(list(Taste)))
        f_cooke_time.write('\n'.join(list(Cooke_time)))
        f_material_desc.write('\n'.join(list(Material_desc)))
        f_share_amount.write('\n'.join(list(Share_amount)))
        f_dishes_title.write('\n'.join(list(Dishes_title)))
        f_agreement_amount.write('\n'.join(list(Agreement_amount)))
        f_tags.write('\n'.join(list(Tags)))
        f_step.write('\n'.join(list(Step)))
        f_material.write('\n'.join(list(Material)))
        f_nutrition_analysis.write('\n'.join(list(Nutrition_analysis)))
        f_production_direction.write('\n'.join(list(Production_direction)))


        f_dashes_name.close()
        f_hard_level.close()
        f_taste.close()
        f_cooke_time.close()
        f_material_desc.close()
        f_share_amount.close()
        f_dishes_title.close()
        f_agreement_amount.close()
        f_tags.close()
        f_step.close()
        f_material.close()
        f_nutrition_analysis.close()
        f_production_direction.close()

        return

if __name__ == '__main__':
    handler = MedicalGraph()

    handler.create_graphnodes()
    handler.create_graphrels()
    # handler.others()

    # handler.export_data()
