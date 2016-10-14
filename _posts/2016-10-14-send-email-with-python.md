---
layout: post
title: 使用Python发邮件
description: 使用Python来发送邮件，在Linux服务器上，连邮件服务也不用安装了，好爽的说
category: Python
keywords: Python, 发邮件
---

工作上又有新需求了……写了个计划任务定期检测某个网站的状态，想着输出日志记录，方便日后备查。但静心再思考，嗯哼……不对，要自己每次主动查日志岂不是很沙雕吗？既然脚本都写了，那就添加功能，一旦出错后，马上发邮件通知自己不就万事大吉了？也能保持时效性。好吧，说干就干，赶紧搭个邮件服务……嘿嘿，不对，发个邮件而已，怎么快怎么来，联想到python有邮件模块，于是有了本文。

<!-- more -->

关于原理部分，此处先不讲，代码如下：

```python
#!/usr/bin/python
#coding:utf-8

import smtplib
from email.mime.text import MIMEText

mail_host = 'smtp服务器地址'
mail_user = '发件邮箱名字'
mail_pass = '发件邮箱密码'
mail_postfix = '邮箱后缀，如qq.com'
to_list = '收件人邮箱地址'
#以上内容根据你的实际情况进行修改

def send_mail(to_list,subject,content):
    me = mail_user+"<"+mail_user+"@"+mail_postfix+">"
    name = mail_user+"@"+mail_postfix
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = me
    msg['to'] = to_list

    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(name,mail_pass)
        s.sendmail(me,to_list,msg.as_string())
        s.close()
        return True
    except Exception,e:
        print str(e)
        return False        
```

注意区分*SSL* 加密 与 普通文本 的不同。

详细的原理讲解，可参考 *廖雪峰* 的 [SMTP发送邮件](http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001432005226355aadb8d4b2f3f42f6b1d6f2c5bd8d5263000) 与 [POP3收取邮件](http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/0014320098721191b70a2cf7b5441deb01595edd8147196000) 