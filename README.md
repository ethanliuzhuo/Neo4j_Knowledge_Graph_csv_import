# 基于菜谱的数据 生成CVS 导入进Neo4j 数据库（以及一些坑）

爬取菜谱的数据文件构成

```bashrc

data          
├── 246
|    └──CommentList.json #评论 不用
|    └──DishesCommensense.json #关键食材和介绍
|    └──DishesMaterial.json #食材、材料
|    └──DishesSuitable.json #替代食材
|    └──DishesView.json #菜谱详细信息，菜名，时间，难度，步骤等
|    └──RecommendLike.json #相关菜
└── 248
|    └──CommentList.json
|    └──DishesCommensense.json
|    └──DishesMaterial.json
|    └──DishesSuitable.json
|    └──DishesView.json
|    └──RecommendLike.json
└── ...         
```
## 1.安装neo4j 数据库
[-**`下载链接`**](https://neo4j.com/download/)<br>

安装至任意盘

## 2.创建一个Graph 数据库
2.1. 打开桌面上的图标
<p align="left">
    <img width="10%" src="image/1.png" style="max-width:10%;">
    </a>
</p>

2.2. 点击 `Add Database`

<p align="left">
    <img width="30%" src="image/2.jpg" style="max-width:30%;">
    </a>
</p>

2.3. 点击 `Crete a Local Graph`,创建一个图数据库

<p align="left">
    <img width="30%" src="image/3.jpg" style="max-width:30%;">
    </a>
</p>

2.4. 输入Name 和 Password, 一般默认Name 为Graph Password 为neo4j或者admin， 密码非常重要，链接数据库时需要密码

<p align="left">
    <img width="30%" src="image/4.jpg" style="max-width:30%;">
    </a>
</p>

2.5. 启动Grph， 点击`Start`, 即启动完成

<p align="left">
    <img width="30%" src="image/5.jpg" style="max-width:30%;">
    </a>
</p>

## 3.数据导入
<p align="left">
    <img width="100%" src="image/6.png" style="max-width:100%;">
    </a>
</p>

经过对比，neo4j的官方命令`neo4j-import`最为强大，速度非常快。接下来我们使用两种方法导入数据：

1.使用Python 文件进行导入

**优点**：对于熟悉python的同学操作更容易理解

**缺点**：速度慢，其本质使用的是和表格中的`create`，经过测试，15,000个菜谱数据导入耗费2个小时左右。建议小规模数据使用。

2.使用`neo4j-import`命令导入

**缺点**：步骤繁琐复杂

**优点**：速度快，相同的数据30秒导入完成

## 3.1 Python 导入

`build_medicalgraph.py`实施。该文件由刘焕勇老师[-**`QASystemOnMedicalKG`**](https://github.com/liuhuanyong/QASystemOnMedicalKG)<br> 修改而来。

