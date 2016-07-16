---
layout: post
title: Python XML解析小结
categories: Python
keywords: python, xml, ElementTree
description: Python中对XML的解析主要有三种方法，分别是SAX、DOM与ElementTree（元素树），最后这种方式较优。
---

在[SVN绑定RTX发送即时消息](http://zshmobi.com/2016/07/14/RTX-And-SVN.html)一文中，参考文章里有提到可以发送即时消息弹窗到指定RTX群，但我在实际环境中，并未看到`SendNotifyBygroup.cgi`这个文件，遂无法实现该功能。查看*RTX SERVER*安装目录下，现有的\*.cgi文件均未有我想要的，遂打算自己动手写个半自动的处理方法——在*RTX SERVER*管理界面，导出所有成员信息，文件格式为*xml* ，好吧，那就顺带把XML这块知识给补上唄。

<!-- more -->

### 什么是XML？

*XML* 意为可扩展标记语言，其设计用来传输和存储数据的，是一套定义语义标记的规则，这些标记将文档分成许多部件并对这些部件加以标识。

**Python对XML的解析**

常见的XML编程接口有*DOM*和*SAX*，解析方法有SAX，DOM，以及ElementTree三种。

- *SAX*

  包含在python标准库，流式读取，比较快，占用内存少

- DOM

​      将XML数据在内存中解析成一个树，一来速度慢，二来比较耗内存

- ElementTree(元素树)

​      它像是一个轻量级的DOM，具有方便友好的API。代码可用性好，速度快，消耗内存少

### ElementTree

使用以下这个XML文件来做例子，假设命名为 `test.xml`

```xml
<?xml version="1.0"?>
<doc>
    <branch name="testing" hash="1cdf045c">
        text,source
    </branch>
    <branch name="release01" hash="f200013e">
        <sub-branch name="subrelease01">
            xml,sgml
        </sub-branch>
    </branch>
    <branch name="invalid">
    </branch>
</doc>
```

接着来看看如何使用*ElementTree*

- **基本用法**

```python
import xml.etree.ElementTree as ET

# 解析文件
tree = ET.ElementTree(file='test.xml')  

# 获取根结点元素
root = tree.getroot()  
"<Element 'doc' at 0x11eb780>"

# 获取标签和属性
print root.tag, root.attrib 
"('doc', {})"

# 对根元素遍历，导找子结点
for child_of_root in root:  
    print child_of_root.tag, child_of_root.attrib 
#branch {'hash': '1cdf045c', 'name': 'testing'}
#branch {'hash': 'f200013e', 'name': 'release01'}
#branch {'name': 'invalid'}

# 根据XML层级数进入指定子结点
root[0].tag, root[0].text 
#('branch', '\n        text,source\n    ')

# 对tree子结点进行深度优先遍历
for elem in tree.iter():
    print elem.tag, elem.attrib
# 只遍历指定标签的元素
for elem in tree.iter(tag='branch'):
    print elem.tag, elem.attrib
```

- 借助XPath

Element 有一些关于寻找的方法可以接受 XPath 作为参数。 find 返回第一个匹配的子元素， findall 以列表的形式返回所有匹配的子元素， iterfind 为所有匹配项提供迭代器。

```python
# 寻找指定层级的标签元素
for elem in tree.iterfind('branch/sub-branch'):
    print elem.tag, elem.attrib

# 寻找指定标签的指定属性
for elem in tree.iterfind('branch[@name="release01"]'):
    print elem.tag, elem.attrib
```

- 建立XML文档

对现有文档内容进行修改

```python
root = tree.getroot()
del root[2] # 删除指定层级标签
root[0].set('foo','bar') # 设置标签内容
```

自行构造

```python
a = ET.Element('root')
ab = ET.SubElement(a, 'child')  # 建立次层级标签
ab.text = "some text"           # 建立标签的内容
b = ET.Element('toor')
top = ET.Element('top')
top.extend((a, b))              # 将a, b两个标签合并到top下
tree = ET.ElementTree(top)      # 构建成ElementTree类，相当于加载文件
```

输出内容

```python
# 打印到屏幕
import sys
tree.write(sys.out)

# 输出到文件
tree.write('filename')
```

- 使用*iterparse*来处理XML流

ET与DOM同样是将XML内容读入内存再处理，那它如何实现高效率与占用内存低呢？有赖于`iterparse`这个工具。

```python
count = 0
for event, elem in ET.iterparse(tree):
    if event == 'keyword':
        if elem.tag == 'tagname' and elem.text == 'textContent':
            count += 1
     elem.clear() # 清除不符合条件的
print count
```

`elem.clear()`是关键，它将不符合条件的元素全部丢弃， 限制内容加载进内存。iterparse生成树时只遍历一次，而parse方法则是首先建立整个树，再遍历来寻找所需要的元素

### 实战应用

回归到本文的主题来，把*RTX SERVER* 导出的XML文件，挑选出指定的元素。先来看看该XML文件的内容「*因原内容过于冗长，作精简处理*」

```xml
<?xml version="1.0" encoding="GB2312"?>
<RTX2005>
  <Database>
    <Sys_User>
      <Item UserName="liergou" Name="李二狗"/>
      <Item UserName="xuergou" Name="许二狗"/>
    </Sys_User>
  </Database>
</RTX2005>
```

每次看到`gb2312`总免不了菊花一紧……疼……按上述ET的方法来直接解析文件，结果杯具了，提示错误诸如*ValueError: multi-byte…*，*not well-formed*，一时间气不打一处来。此时心想，要不走个弯路吧，把我大RE正则摆上台……

```python
import re
p = re.compile('.*?UserName="(.*?)".*?Name="(.*?)".*?',re.S)
with open('rtxexport.xml','r') as f:
    lines = f.readlines()
    for line in lines:
        if 'UserName' in line:
            content = re.findadll(p, line)
            for item in content:
                print '账号: ' %item[0]
                print '姓名：' \
               %item[1].decode('gb2312').encode('utf-8')
```

“你这不是在装逼吗？” 这位同学，你大胆发言的行为真让我感动，你可以坐下来了。这尼玛确实有点蛋疼啊。好吧，那就现学现卖，把ET给弄上。

*暂时能想到的方法是先读，处理好编码再写入新文件*来处理。废话不多说，直接上代码。

```python
#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys                                                                      
import xml.etree.ElementTree as ET

reload(sys)
sys.setdefaultencoding('utf-8')

with open('rtxexport.xml','r') as f:
    lines = f.readlines()
    with open('newfile.xml','w+') as l:
        for line in lines:
            line = line.decode('gb2312','utf-8')
            if 'GB2312' in line:
                # 记得要把声明编码那行替换成utf-8噢
                line = line.replace('GB2312','utf-8')
            l.write(line)

tree = ET.ElementTree('newfile.xml')
for line in tree.iter(tag='UserName'):
    try:
        print '%s - %s' %\
        (line.attrib('UserName'),line.attrib['Name'])
    except KeyError:
        pass
```

RTX用户名与账号均获取成功，同理，可以获取部门信息、群组信息。把同一部门、同一群组的账号使用`,`串连，在`post-commit.py`脚本中，把`reciever=%s`指定到所获取的部门、群组字符串，即可实现和指定部门、指定群组发送即时弹窗消息了。

> [XML解析](http://www.ziqiangxuetang.com/python/python-xml.html)
>
> [ETree官方文档](https://docs.python.org/2/library/xml.etree.elementtree.html)
>
> [python程序员周刊之XML](http://pycoders-weekly-chinese.readthedocs.io/en/latest/issue6/processing-xml-in-python-with-element-tree.html)

