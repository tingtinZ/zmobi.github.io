---
layout: post
title: MySQL导出csv文件的小结
category: 数据库
description: 关于MySQL数据库导出csv格式文件的小结，以及csv在使用中存在的乱码问题
keywords: MySQL, csv, python, 导出csv文件， csv乱码
---

鉴于近期需要经常从数据库中导出数据发给同事，而原本后台应该集成的功能，由于某些原因未能从根本上解决，只能暂时由我手工代替。本着以懒为本的宗旨，遂斟酌一番，写个脚本来处理，免得再生事端。

<!-- more -->

要实现从MySQL数据库中导出csv文件，有两种实现的方式，一种是借助数据库的`SQL`语句来实现，第二种是借助 `Python` 。两者各有优劣，且听洒家娓娓道来。

## SQL语句生成CSV

将所要数据 *Select* 出来，写入到指定文件，输出时，预定制为csv文件的格式，即

```sql
select * from table_name
-- 写入到指定文件
into outfile '/tmp/your_export_file.csv'
-- 设置输出到文件时的编码「在win系统使用该csv文件时需要写上」
CHARACTER SET gbk
-- 格式化成csv的形式
fields terminated by ',' optionally enclosed by '"' escaped by '"'
lines terminated by '\r\n' 
;
```

如此一来，导出的csv文件能够直接在windows系统中使用，不会产生乱码；如果导出的文件是在 *MacOS* 或者是 *Linux* 使用则编码要改成 *UTF-8* 。

P.S：特别注明，**Ubuntu 16.04** 安装的 *MySQL* 默认不支持输出到文件，解除限制的话，请做如下更改

```shell
sudo echo 'secure_file_priv=""' >> /etc/mysql/mysql.conf.d/mysqld.cnf 
```

最后评价此法的优劣；兴许其劣势也有解决方案，探究这事，还是交给别人吧。

- 优势：编码转换无痛解决
- 劣势：导出的文件缺乏表头，查看时略为不便

## Python导出CSV

实现此法的两个前提，机器上得安装有Python的两个模块，分别是 `MySQLdb` 与 `csv` ；后者是包含在标准库，难点在于前者。特别是在 `CentOS` 的机器安装最为蛋疼，此处以其为例子讲解。

```
# 注意区分大小写，否则无法安装
yum install MySQL-python

# 解决手动升级Python2.7后，上述模块仍然无法导入的问题
# import MySQLdb时报错： “没有libperconaserverclient.so.18"
ln -s /usr/local/mysql/lib/libperconaserverclient.so.18 /usr/lib64/libperconaserverclient.so.18
```

回归到正题，借助 *CSV* 模块即可轻松实现导出，具体如下：

```python
import MySQLdb
import csv

# 连接数据库
conn = MySQLdb.connect(user='db_user', passwd='db_password', host='127.0.0.1')
cur = conn.cursor()
# 查询并导出
cmd = 'selct * from table;'
cur.execute(cmd)
with open('export_csv_file.csv', 'wb') as csv_file:
    csv_writer = cur.writer(csv_file)
    # 添加表头信息
    csv_writer.writerow([i[0] for i in cur.description])
    csv_writer.writerows(cur)
cur.close()
conn.close()
```

其优劣势则是：

- 优势： 可添加表头信息
- 劣势： 编码问题特别蛋疼

数据库默认的是 *UTF-8* 编码，写入时必须同样以 *UTF-8* ，若想转成 *GBK* ，则可能要在写入时重新reload系统编码，设置为 *GBK* ；但个人认为这种做法欠佳。

暂时无自动便捷的方法可以将其转成 *GBK* 编码，但手工转换还是可以的，在 *windows* 系统在使用 **notepad++** 来修改即可。