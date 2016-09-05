#! /usr/bin/python
# -*- coding: utf-8 -*-

import cgi, cgitb
import MySQLdb
import os
import sys

def get(name):
    conn = MySQLdb.connect(host='localhost', user='root', passwd='notjeffchan', db='kaoqin', use_unicode=True,charset='utf8')
    cur = conn.cursor()
    """
    get_gnum = "select gnum from user where name='%s';" % name
    cur.execute(get_gnum)
    gnum = cur.fetchone()
    """
    reload(sys)
    sys.setdefaultencoding('utf-8')
    cmd = "select name,date,weekday,start,stop,total from record07 where name = '%s' order by date;" % name
    cur.execute(cmd)
    for line in cur.fetchall():
        if line[3] == line[4]:
            print '<p><span>%s</span><span>%s</span><span>%s</span><span id="green">%s</span><span id="green">%s</span><span>%s</span></p>' % (line[0],line[1],line[2],line[3],line[4],line[5])
        else:
            print '<p><span>%s</span><span>%s</span><span>%s</span><span>%s</span><span>%s</span><span>%s</span></p>' % (line[0],line[1],line[2],line[3],line[4],line[5])


# 创建 FieldStorage 的实例化
form = cgi.FieldStorage()

# 获取数据
name = form.getvalue('name')
# month = form.getvalue('month')


print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print '<link rel="stylesheet" href="../check.css" type="text/css" />' 
print "<meta charset='utf-8'>"
print "<title>处理结果页</title>"
print "</head>"
print "<body>"
print "<header>"
print "<h2>考勤查询结果</h2>"
print "</header>"
print '<div class="result">'
print "<p><span>姓名</span><span>日期</span><span>周几</span><span>开始打卡</span><span>结束打卡</span><span>完整记录</span></p>"
get(name)
print "</div>"
print "</body>"
print "</html>"


