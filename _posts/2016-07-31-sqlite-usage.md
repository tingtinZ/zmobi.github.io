---
layout: post
title: SQLite快速上手
description: 快速学习SQLite小型数据库
category: 数据库
keywords: SQLite, Python
---

## 是什么？

*SQLite*是什么？它是一种自我包含、无须启动服务、无需配置文件的事务型数据库。*SQLite* 是免费开源的，其代码可用于在网上找到，任何人能以任何目的使用它。

*SQLite* 同时是一款嵌入式数据库引擎，其直接读写系统磁盘上的数据库文件。一个完整的SQLite数据库，包括多个表格，索引、触发器和视图均包含在一个单独文件中。*SQLite* 支持多平台，如*windows* ,  *MacOS* , *linux* ，以及*android* 。

<!-- more -->

什么情况可以选择使用*SQLite*呢？[官网上的解释](http://www.sqlite.org/whentouse.html) 是，只要你的数据库 *读写与数据库均同一设备的* 、*对读写时效性要求低的* 、*数据量较小的* 均可使用。

## 怎么用？

- 安装

linux 可以直接安装

```shell
# fedora
yum install sqlite3

# ubuntu
sudo apt-get install sqlite3
```

*Windows* 平台则到[官网](http://www.sqlite.org/download.html)下载

*MacOS* 默认安装了*SQLite*

- SQLite命令

使用时，要区分两种形式的命令：一种是通用SQL命令，一种是SQLite独有的

创建、备份与恢复数据库

```shell
# 创建or打开数据库
sqlite3 test.db

# 备份数据库
sqlite3 test.db .dump > backup.sql

# 恢复数据库
sqlite3 test.db < backup.sql
```

建表、增删改等操作

```sql
-- 以下是通用SQL命令
-- 创建表格
create table rtx(name varchar(40) not null, account varchar(40) not null);

-- 插入数据
insert into rtx(name, account) values('测试', 'test');

-- 更新数据
update rtx set name = '我不是测试' where account = 'test';

-- 删除数据
delete * from rtx ;

-- 查询数据
select * from rtx;
```

特殊命令「.command」

以下是SQLite独有的命令,以.开头的，只讲几个常用的，想了解更加详细的命令，可以参阅[官网说明](http://www.sqlite.org/cli.html)

```sql
-- 查看表结构
.schema [table name]

-- 查看所有表
.tables

-- 查看当前状态
.show

-- 导出数据库到SQL文件
.output [filename]
.dump

-- 从SQL文件导入数据库
.read [filename]

-- 查询结果显示标题
.headers on

-- 显示查询结果的格式 「默认是list, 选column则为Mysql的格式」
.mode [list | html | column | csv ]

-- 导入数据到表格
-- 01 从mysql中select * from table into outfile 'xxxx.txt'
-- 02 把xxxx.txt中的制表符换成,号
.separator ","    
-- 03 把xxxx.txt文件放在sqlite文件放在同一目录中
.import xxxx.txt table_name
```

## Python操作SQLite

目前python标准库均已支持sqlite，使用方法如下：

```python
import sqlite3

# 连接数据库
conn = sqlite3.connect('db_name')
cur = conn.cursor()

# 查询
cur.execute('select * from table_name')
cur.fetchall()

# 删除数据
cur.execute('delete * from table_name')

# 断开连接
conn.commit()
cur.close()
conn.close()
```

如果还是没弄懂如何操作SQLite数据库，可以借助[SQLite Browser](http://sqlitebrowser.org)

> [SQLite简介](http://www.sqlite.org/about.html)
>
> [SQLite书籍](http://www.sqlite.org/books.html)
>
> [SQLite命令详解](http://www.sqlite.org/cli.html)
