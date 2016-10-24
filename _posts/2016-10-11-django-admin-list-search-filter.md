---
layout: post
title: django后台外键的显示、查询与过滤
description: 在django后台中，添加显示外键的字段，使其能够支持通过外键查询与过滤
category: Django
keywords: django, admin, foreginkey, list_display, search_field, list_filter
---

当把表建成功之后，如何在后台中对已经设置外键的表格进行联表查询呢？经过挊主一番调查，终于摸清楚门道了，但此解决方案仅是目前所知，日后有更为规范的操作再更新吧

<!-- more -->

## Models

首先是表格设置，如下： 

```python
# 用户简表
class Simple(models.Model):
    gnum = models.IntegerField()
    name = models.CharField(max_length=100)

# 用户详表
class Detail(models.Model):
    num = models.ForeignKey(Simple, on_delete=models.CASCADE)
    tel = models.IntegerField()
```

## list_display

### 方法一：

在*models.py* 中添加自定义方法

```python
# Detail中添加
def name(self):
    return u'%s' % self.num.name
```

接着在*admin.py* 的*list_display* 中添加 **name**  即可

### 方法二：

在*admin.py* 中定义方法

```python
class DetailAdmin(admin.ModelAdmin):
    list_display = ('num', 'get_name', 'tel')
    
    def get_name(self, obj):
        return obj.num.name
    get_name.admin_order_field = 'num' # 允许以该字段排序
    get_name.short_description = 'User Name' # 重命名字段名字
```

## search_fields

设置搜索字段，[官网文档](https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields) 中教的方式：通过 `表名__字段` 来访问是无效的。应该直接通过关联外键的那个字段进行反查。

```python
# 在DetailAdmin下添加
search_fields = ['num__name']
```

## list_filter

原理同上

```python
# 在DetailAdmin下添加
list_filter = ['num__name']
```

## 小结

~~目前还存在的疑问是，为毛不能够像实际的sql语句访问那样显示联表查询的多个值呢？即关联号码，在 *用户详表* 中不能直接编辑、显示 *用户简表* 中的姓名呢？~~

大爷的，突然间茅塞顿开，知道问题出在哪里了。

```python
# models.py 中定义的默认返回值
def __unicode__(self):
    return self.xxxx # 此处返回你想要的字段
# 该字段会默认为引用外键时的显示默认值
```

注意，*list_display* 所展示的字段必须是在数据库接口语句中，能够真正被查询得到的；而 *search_fields* 与 *list_filter* 则是以私有函数定义的。使用时注意区分两者。
