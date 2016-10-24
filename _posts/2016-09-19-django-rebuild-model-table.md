---
layout: post
title: django重建表格
category: ['Django', 'Apache']
description: 重建django中原有设定的model表格
keywords: django, rebuild, 重建表格
---

刚建立的Model表格，某个字段漏了或者设置错了怎么整？默认的`sqlite`不支持修改字段，而且django本身也不支持此种操作，那怎么整 ？


```shell
# 删除应用目录下的migrations目录
rm -rf your_app_name/migrations

# 删除数据库中相关表的记录
DELETE FROM django_migrations WHERE app = 'your_app_name'

# 删除应用中创建过的表
drop table your_app_tables

python manage.py makemigrations your_app_name

python manage.py migrate
```


## 修改日期显示格式

```shell
# 修改setting.py的配置
USE_L10N = False
DATETIME_FORMAT = 'Y-m-d H:i:s'
DATE_FORMAT = 'Y-m-d'
```


此法仅支持*django 1.9.5* 以上版本
