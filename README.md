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

2.2. 点击 (`Add Database`)

<p align="left">
    <img width="30%" src="image/2.jpg" style="max-width:30%;">
    </a>
</p>

