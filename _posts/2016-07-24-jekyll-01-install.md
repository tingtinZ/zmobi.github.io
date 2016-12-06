---
layout: post
category: Jekyll
description: jekyll系列教程之一，简介与安装
title: Jekyll教程01-简介与安装
keyword: Jekyll教程
---

## 简介与安装

### *缘由*

为何要写这个系列的文章呢？一是为了检验自己所学，二是为了方便日来查阅，三是为了方便他人。文章的逻辑是从一个新手的角度，阐述了如何逐步了解并掌握jekyll博客；同时建议阅读下志愿者们翻译的说明文档。

<!-- more -->

### *Jekyll是什么？*

Jekyll 是一个简单的博客形态的静态站点生产机器。它有一个模版目录，其中包含原始文本格式的文档，通过一个转换器（如 [Markdown](http://daringfireball.net/projects/markdown/)）和我们的 [Liquid](https://github.com/Shopify/liquid/wiki) 渲染器转化成一个完整的可发布的静态网站，你可以发布在任何你喜爱的服务器上。Jekyll 也可以运行在 [GitHub Page](http://pages.github.com/) 上，也就是说，你可以使用 GitHub 的服务来搭建你的项目页面、博客或者网站，而且是完全免费的。

### *如何安装？*

此处以*Ubuntu 16.04* 为例子说明，以下是详细的操作步骤

```shell
sudo apt-get update

# 安装ruby
sudo apt-get install ruby ruby-dev

# 安装nodeJS
sudo apt-get install nodejs

# 安装make gcc gcc+ ，安装jekyll需要使用
sudo apt-get install make gcc gcc+ build-essential

# 安装jekyll
# 会自动安装liquid，kramdown, yaml, sass和rouge
sudo gem install jekyll
# 如果上述命令很久都没反应，请更换gem源
sudo gem sources --remove http://rubygems.org/
sudo gem sources -a https://ruby.taobao.org/

# 检查下python 和 ruby的版本
# python >= 2.7 ; ruby >= 1.9.3
ruby -v
python -V
```

### *如何使用jekyll?*

安装完毕之后，如何迅速地使用jekyll呢？想把博客放到github上？别急，咱们先以本地调试的形式来展开对jekyll的学习。

新建一个博客并启动开发服务器

```shell
# 新建
jekyll new myblog
# 进入目录
cd myblog
# 启动开发服务器进行预览
jekyll serve -H 0.0.0.0
```

接着在同一局域网内的设备，用浏览器打开`http://your_ubuntu_server_ip:4000/`

<img src="/res/img/in_posts/jekyll-01-blog_index.png" />

看到首页了，是不是很激动人心呢？

### *关于Jekyll命令*

jekyll命令你只需要知道如何*新建* 与 *启动服务* 即可

**新建**

```shell
# 这里假设新建为myblog
jekyll new myblog 
```

**启动服务**

```shell
jekyll serve
```

默认会自动监测文件是否有变动，且自动再生成

默认端口为4000，且只能在本机使用*http://127.0.0.1:4000*访问

默认把*myblog* 目录下的内容生成 *./_site*目录中

考虑到*serve* 比较容易记错，可使用`server`进行替代，不影响使用

**其他选项**

```shell
# 指定生成目录名，不在myblog生成.site
# 注意指定的目录非空，则生成时会清空该目录下的所有文件
jekyll serve -d 'your_directory' 

# 脱离终端放到后台运行
# 运行后，终端上有提示如何杀死进程 kill -9 '进程号'
jekyll serve -B

# 不监测文件变化
jekyll serve --no-watch

# 脱离本机访问限制
jekyll serve -H 0.0.0.0

# 修改默认端口
jekyll serve -P '你想要的端口号'

# 支持预览草稿
jekyll serve --drafts
```

建议不要放到后台去运行，这样可随时查看日志，方便查找问题，老司机请无视

经常运行一长串命令很麻烦？自建个别名快捷命令吧

```shell
# 编辑用户bash环境
vim ~/.bashrc

# 添加别名
alias jlocal='jekyll serve -H 0.0.0.0 --drafts'

# 使其生效
source ~/.bashrc
```



好了，是时候写篇文章表达此时的心情到*myblog* 里去吧。接下来说说如何写文章
