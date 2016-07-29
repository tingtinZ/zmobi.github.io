---
layout: post
categories: RTX
title: RTX实现@功能
description: 在RTX通过监控聊天记录来实现@功能，当@人名后，会发送弹窗通知提醒相应人员
keywords: RTX, @功能, RTX实现@功能
---

最近有同事提议，能否在RTX上实现@功能，即类似QQ那样——*@人名* 实现特别提醒，当时哥临危不乱，从容蛋定地回答了一句：“容老夫三思”。经过一番调研与摸索，终于折腾出解决方案了。但……是……只能说……不太完美吧。

<!-- more -->

## 实现思路

设想步骤如下：

1. 在RTX聊天窗口中，输入@人名
2. 当聊天记录中出现@人名后，自动发送弹窗消息

对此再进行细分

- 如何排查RTX聊天记录中是否出现@字符呢？
- 如何确定是谁想@谁呢？

继续分解任务

- 是否能够监控聊天记录？
- 是否能够实时发送弹窗？
- 是否需要定时执行呢？

接着对上述三个任务作调研，看能否实现。

### 一、是否能够监控聊天记录

RTX本身不支持聊天记录的实时查看，鉴于本人不了解RTX实际的运行机制，官网上查找其支持的插件，居然有个免费的[消息监控插件](http://rtx.tencent.com/rtx/download/rtxfd_13.shtml) ，于是赶紧下载安装试用。

1. 解压下载的安装包，得到文件`AppIMWatch.dll` 
2. 把文件拷贝到**RTX SERVER** 的目录`C:\Program Files (x86)\Tencent\RTXServer\bin`。
3. 在**RTX 管理界面** 中，点击`应用管理器 => 启动RTX应用管理器 => 选择添加应用=> 选中AppIMWatch.dll`即可  
4. 自动生成监控目录，即`C:\Program Files (x86)\Tencent\RTXServer\IMWatch`
5. 聊天记录文件格式为`IM_2016-07-22.txt` ，内容为是

```python
ThreadID=5020               # 线程ID
Time=2016-06-22 10:17:48    # 对话时间
Sender=liergou              # 发送者账号
Receivers=dabiaoge          # 接收者账号
Msg=你根本不是司机           # 对话内容
```

很好，聊天记录已经出来了，已经包含发送者和接收者的信息。那么问题来了，如何对它进行监控呢？怎样才能知道它是否有更新呢？脑子里第一时间想到的是`watchdog` 库，监控文件变化，经过一番测试，我发现一个大BUG。这尼玛在瘟系统根本没办法监控，即便使用`pywin32`库也无效。静下心来想想，聊天记录文件这个进程一直在等待输出，文件上没办法实时显示，需要手动刷新才会触发监控动作。*IMWatch*应该是一个持续写的动作， 根本没法监控；不像是单个修改完成后，就退出，此时才能正常触发`watchdog`的监控机制。与此同时得出一个结论，在RTX聊天窗口中发送的消息，需要有一定的延时才能写入到`IM_2016-07-22.txt`文件中，即时发送弹窗提醒无法实现，只能延时处理了。回归到问题来，如何对聊天记录文件进行监控呢？暂时想不出来，继续下一步吧。

### 二、是否能够实时发送弹窗

在<a href="/2016/07/14/RTX-And-SVN.html">SVN绑定RTX发送即时消息</a>一文，已经说明如何实现发送弹窗消息了。接下来需要做的，仅仅是获取接收者的账号，消息内容包含@字符即可。处理逻辑为：

1. 抓取最新那条聊天记录
2. 判断消息内容是否有@
3. 判断账号名是否有异常
4. 发送友好的弹窗内容

**抓取最新那条聊天记录**

使用`open(file, 'r')` 读取聊天文件，只抓取最后一栏的记录。但这样写代码好像略疼。嗯哼？等等……结合最近学习的爬虫内容，倘若把聊天记录文件通过http协议的方式来访问不就可以了吗？定时访问聊天记录文件，所有内容均为一行字符串，再通过正则抓取最新的那条记录不就可以了嘛。一举两得，把监控文件变化也给解决了，嘿嘿。但是……等等……那岂不是又得搭个`apache`服务实现*http*协议访问了？ 不用啊，结合<a href="/2016/07/21/share-files-with-hfs.html">傻瓜式局域网文件共享</a>就可以了啊！*提醒一点，HFS添加`IMWatch` 目录时，记得加密，不然聊天内容谁都可以查看* 。

**判断消息内容是否有@**

如果是@李二狗这种形式，我发现不好判断，我哪知道人名到哪里才断开呢？QQ上的按完@后，直接出来人名列表你选，而当前RTX的环境，算是半开发吧，在现有基础上做修改而已，无法完美实现同样的功能，无奈，只能使用 `@李二狗@` 的形式咯。以下是部分实现的代码

```python
import time
import requests
import re

today = time.strftime("%Y-%m-%d")
# Name , Pass 是在HFS中设置的目录加密用户名和密码
url = 'http://%s:%s@10.0.0.10:2000/IMWatch/IM_%s.txt' %(Name, Pass, today)
html = requests.get(url, timeout=2)
if html.status_code == 200:
        content = html.content
        items = re.findall('\r\nTime=(.*?)\r\nSender=(.*?)\r\nReceivers=(.*?)\r\nMsg=(.*?)\r\n', content)
        msg    = items[-1][3].decode('gb2312').encode('utf-8')
        sender = items[-1][1]
        sendto = items[-1][2].rstrip(';')
        sendtm = items[-1][0]
        if '@' in msg:
            print '发送弹窗消息'
```

**判断账号异常与发送友好消息** 

这两处主要是通过*rtx账号*获取真实姓名，发送弹窗消息时，能够显示 *李二狗向你发送了弹窗消息*  的内容。

通过查看目录`C:\Program Files (x86)\Tencent\RTXServer\WebRoot` ，我发现了一个问题，既然发送弹窗消息是调用`SendNotify.cgi` ，同理，其他`*.cgi` 文件应该也能派上用场。简单阅读了`GetMobile.cgi` 文件后，我发现只要修改以下的数值，便可获取不同的信息

```php
// 5 是获取用户的手机号
$Result->GetKeyValue(5, $vName, $vValue);
// 6 是获取用户的真实姓名，即中文名字
$Result->GetKeyValue(6, $vName, $vValue);
```

因此，拷贝*GetMobile.cgi* ，重命名为`GetUserName.cgi` ，只获取用户姓名。则发送弹窗消息时，内容可以很友好地显示*【召唤通知】【李二狗】释放了[RTX弹窗技能]召唤了你关于【XXX】的内容* 。

### 三、是否需要定时执行

看到这里，咱们先把前面的流程再理顺一次。

1. 写个程序，定时监控RTX聊天记录，获取最近的记录
2. 当聊天内容出现@人名@时
3. 编辑好弹窗消息
4. 延时发送弹窗消息

这里头还有问题需要解决，如果两三个人同时发送带有@人名@的消息，如何筛选出来，并且每条弹窗消息都能发送出来呢？RTX在下班后，上班前均无人使用，如果程序一直跑，有点浪费资源。每天通过RTX发送第一条消息后，当天的聊天记录文件才会生成。因此，此程序是需要定时执行的，即每天上班后跑，下班后12点时停止运行，还等什么，赶紧到瘟系统添加计划任务吧。

### 四、小结

如文章开头所说，虽然功能上是实现了，但不太完美，目前只能将就着用吧。做个小结，该程序的优点是……功能实现了，呵呵。缺点是：*依赖RTX消息监控插件，它是本功能得以实现的最重要前提*，*依赖HFS提供http协议访问消息记录文件*， *有点消耗资源的嫌疑* 。另外，该程序单条聊天记录中目前仅支持@一个人名，弹窗消息有所延迟，这便是站在他人基础上进行半开发的宿命啊……

最后的最后，献上代码

```python
# -*- coding: utf-8 -*-

import requests
import urllib2
import time
import re
import sys

Info = {'Name': 'zshmobi', 'Pass': 'zshmobi'}  # hfs.exe 用户名账号
TT = [ 'f', 'u', 'c', 'k', 'u' ]   # 用来解决循环执行时，略过已经发送过的弹窗消息

def GetName(account):
    ''' 通过RTX账号获取用户真实姓名，获取结果字符集为gb2312，要转成utf-8 '''
    url = 'http://10.0.0.10:8012/GetUserName.cgi?receiver=%s' % account
    html = urllib2.urlopen(url)
    username = html.read().decode('gb2312').encode('utf-8') 
    return username

def SendInfo(sendto, msg):
    ''' 发送弹窗消息 '''
    url_pre = 'http://10.0.0.10:8012/SendNotify.cgi?'
    url_aft = 'title=召唤提醒&delaytime=10000&receiver=%s&msg="%s"' % (sendto, msg)
    url = url_pre + url_aft
    urllib2.urlopen(url)
    #print '召唤成功'

def GetInfo(line):
    ''' 编辑好待发送的弹窗消息 '''
    NameDict = {}
    msg = line[3].decode('gb2312').encode('utf-8')
    sender = line[1]
    sendto = line[2].rstrip(';')  #当接收者为群成员时，最后会有个;号，去除掉
    sendtm = line[0]

    SenderName = GetName(sender)  # 获取发送者姓名
    for account in sendto.split(';'):
        username = GetName(account)
        NameDict[username] = account
    NameDict[SenderName] = sender  # 该字典作用是通过姓名反查账号
    result = re.match('.*?@(.*?)@.*?', msg)
    try:
        Name = result.group(1) # 只获取格式为 @人名@ 的结果，单个@则出错
        try:
            if Name == 'all' or Name == '全体成员' or Name == '全体':
                Receivers = sendto.replace(';', ',') # 前面去掉最后;号的作用在此
            else:
                Receivers = NameDict[Name]
        except KeyError:
            print 'no accout that named by %s' % Name

        NewMsg = '【%s】召唤了你关于【%s】' \
                %(SenderName, msg.replace(' ', ''))  #去除空格，否则消息显示不完整
        # 在窗口中打印消息记录，好方便查看究竟都发送了哪些召唤请求
        print '%s %s @ %s : %s' % (sendtm, sender, sendto, msg.replace(' ', ''))   

        TT.pop()  # 去除末尾
        TT.insert(0, sendtm) # 添加新的发送时间
        SendInfo(Receivers, NewMsg)
        time.sleep(1)  # 暂停1秒，否则2~3秒内发送给同一个的弹窗消息会被覆盖掉
    except AttributeError:
        pass

def Main():
    today = time.strftime("%Y-%m-%d")
    url = 'http://%s:%s@10.0.0.10:2000/IMWatch/IM_%s.txt' % (Info['Name'], Info['Pass'], today)
    try:
        html = requests.get(url, timeout=2)
        if html.status_code == 200:
            content = html.content
            items = re.findall('\r\nTime=(.*?)\r\nSender=(.*?)\r\nReceivers=(.*?)\r\nMsg=(.*?)\r\n', content)
            if len(items) < 5:
                total = len(items)
            else:
                total = 5
            for num in range(total):
                num = num-total
                if '@' in items[num][3] \
                    and '【图片' not in items[num][3].decode('gb2312').encode('utf-8') \
                    and items[num][0] not in TT :
                    GetInfo(items[num])
        elif html.status_code == 404:
            # 当天的聊天记录还未生成
            pass
    except requests.ConnectionError:
        title = '【失效通知】'
        msg = '[%s]HFS服务被关闭' % (time.strftime("%Y-%m-%d %H:%M:%S"))
        sendto = 'zshmobi'  # 设置为管理员的账号，当HFS服务挂掉后，通知处理
        pre = 'http://10.0.0.10:8012/SendNotify.cgi?'
        afk = 'title=%s&receiver=%s&msg=%s' % (title, sendto, msg)
        purl = pre + afk
        urllib2.urlopen(purl)
        sys.exit()

if __name__ == '__main__':
    print '我是RTX @功能，请忽关闭我，亲'
    while True:
        Main()
        time.sleep(2)
```



> [Watchdog库的介绍](http://sapser.github.io/python/2014/07/25/watchdog/)
