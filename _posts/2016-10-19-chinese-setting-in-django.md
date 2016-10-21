---
layout: post
title: 关于django的中文化
category: Django
desriptions: 关于django中可以设置中文化的地方，主要是后台设置
keywords: django, admin, 后台, 中文化
---

针对近期解决的*Django* 中文化以及部分小技巧做一个小小的总结，方便日后查询回顾。暂不做系统性总结，以后可能会考试翻译下官方文档中的快速上手章节。本修改基于Django 1.10。

<!-- more -->     

### 后台中文化

#### 界面的中文化

编辑*setting.py* ，在 *中间件MIDDLEWARE* 中添加

```python
'django.middleware.locale.LocaleMiddleware',
```

#### 模板中文化

默认的django后台，均显示*django administration* 略为单调，其实是可以自定义的。

编辑 项目目录下的 *urls.py* ，在末尾添加这三项，自行体现下效果吧

```python
admin.site.site_header = u'我是后台标题'
admin.site.index_title = u'我是站点管理'
# 后台中的 查看站点，设置你想要跳转的链接
admin.site.site_url = 'http://www.so.com'
```

#### 应用的中文化

要想让后台查看创建的应用也能实现中文化，在新版本中才能实现，添加应用的写法将有所改变。

编辑*setting.py* ，在 *INSTALL_APPS* 中修改

```python
# 旧有的添加应用写法
'appname',

# 新的添加应用写法
'appname.apps.appnameConfig',
```

接着在对应的应用下 ，编辑 *appname/apps.py* ，在类的末尾添加

```python
verbose_name = u"你想要的应用名字"
```

#### 表名的中文化

修改相应的*models.py* 文件即可 ，在定义的*Meta* 中指定

```python
class Meta:
	verbose_name = u'单数名字'
	verbose_name_plural = u'复数名字'
```

#### 字段的中文化

定义字段时，添加 *verbose_name* 即可 



### 其他配置

主要是围绕 *setting.py* 进行说明、

#### debug模式

如果关闭时，注意允许访问来源的设置

```python
ALLOWED_HOSTS = ['*',]
```

#### 时间显示

```python
# 显示当前时区时间
TIME_ZONE = 'PRC'
# 是否使用拉丁语文本
USE_L10N = False
# 设置时间格式 
DATETIME_FORMAT = 'Y-m-d H:i:s'
# 设置日期格式
DATE_FORMAT = 'Y-m-d'
```

#### 静态文件收集

默认指定的是 *static* ，如果你想自定义也可以 

```python
#默认的
STATIC_URL = '/static/'

# 自定义的写法
STATIC_ROOT = os.path.join(BASE_DIR, "collected_static")
```