---
layout: post
category: 效率
title: WIN10中Pycharm的配置
description: 在win10系统中对pycharm进行简单配置，让其支持markdown，git与github，方便代码的管理
keywords: pycharm, windows, win10, git, github, markdown
---

## 缘由

对于编辑器圣战这玩意，我估计得靠边站，没啥话语权。本人奉行简单即可，拿来即用，别整那些没用的「明显自己不懂罢了」。一周之前安装的pycharm，在win10中运行好几次后，便没了使用的冲动，主要是嫌弃其启动慢，过于臃肿。鉴于windows系统的尿性，在该环境学习python非常蛋疼，加之熟悉了类unix系统良好的操作特性，特别是git，无奈，只能在WIN10中装个虚拟机跑Ubuntu来学习。虽说直接在服务器中修改代码能够胜任，但vim模式下，修改内容过多时，不免隐隐作痛。直接在ubuntu中装个sublime text 2吧，却又不支持中文，网上有解决方案，可老是折腾来去的，徒增烦恼，并且浪费时间。霎那间，macbook在心中争得首位，其次ubuntu，最后才是瘟到死，啧啧。

<!-- more -->

之前有听闻的方案，说有个啥软件来着，可以把linux的目录挂载到windows，也找到该篇文章观摩，啧啧，一个字……疼。无意间再次打开pycharm，提示有版本更新，点击后打开浏览器跳转至官网。鉴于最近两周有在啃英文文档，再次看到整个网站的英文，有点略为享受的滋味。官网上的[简介网页](http://www.jetbrains.com/pycharm/documentation/)有八小段视频，需要科学上网观看。靠着自己战五渣的英文水平，外加youtube支持cc英文字幕，勉强啃完。好家伙，这才进一步了解Pycharm的牛逼之处。另外该网页上还附带不同平台下的快捷键操作，以及完整版的官方说明书。

pycharm完美地解决了我心中的顾虑。支持github与git的同步，可以让我方便地更新jekyll博客的内容；与此同时，我先前在服务器中搭建私有的git服务，也能够同步仓库，在win10中修改完提交推送后，在内网机器再pull下来，测试使用。另外pycharm也有支持markdown的插件，原来使用的typora估计可以下岗了。

## 具体实施

#### 安装git

我选择安装的是[msysgit](https://git-for-windows.github.io) ，下载后安装，过程中有问我是否选择完整地安装unix命令，是的话会覆盖掉dos相应的命令「因为没截图，只能说个大概」，我当然很装逼地选择是。

#### 生成ssh key

安装完毕后，在桌面右键进入 git bash界面

```shell
# 查看当前目录命令
$ pwd

# 进入git用户主目录，通常是windows用户的主目录
# 例如你瘟系统名字是 zshmobi
# 目录就是 c:\users\zshmobi
$ cd ~

# 建立.ssh目录
$ mkdir -pv .ssh

# 生成ssh key，如果你不能执行下述命令
# 请先安装cygwin；-C 是添加KEY的注释，方便管理Key
# 之后会问你是否设置密码，跳过即可
$ ssh-keygen -t rsa -C "name@servername"
```

接着用文本编辑器打开公钥，粘贴到github或者是自建的git服务器中吧。

#### 设置git与github

在Pycharm中，依次打开如下窗口

`File` => `setting` => `Version Control` 即可看到git与github。

github的设置是

```python
Host: https//github.com
Login: your accout name
Password: your password
选中  Clone git repositories using ssh
```

git的设置是

```python
Path to Git executable:  选中git.exe的路径
```

#### 同步与提交

在`Project`窗口中选中项目或者文件，依次点击`VCS` => `Git`  即可看到提交选项。

克隆仓库则为 `VCS` => `Checkout from Version Control` 

#### markdown插件

`File` => `setting` => `plugins` => `install JetBrains plugin` ，搜索markdown即可。 

#### VCS.XML文件

在Pycharm中管理git仓库,则会在`Project`窗口下第一个仓库目录下建立`.idea/vcs.xml`文件, pycharm全靠它来管理代码变更,因此要事先在仓库的**.gitignore**文件中添加过滤*.idea*目录。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="VcsDirectoryMappings">
    <mapping directory="$PROJECT_DIR$" vcs="Git" />
    <!-- 映射到哪个目录 使用什么版本管理工具 -->
    <mapping directory="E:\wtuse" vcs="Git" />
  </component>
</project>
```

## 小结

以上便是本人关于pycharm设置的全部，后续如果有时间会考虑再更新。pycharm之所以不出汉化，我认为是没必要。这也是我在阅读多数英文文档后的感悟，一是软件变更之处太多太快，二来汉化后不利用软件的使用与传播，三是原版英文的说明，有时会更胜于汉化后的效果。

最后，说说Pycharm的好处吧：

1. 支持python包管理
2. 支持多种文档测试
3. 代码操作快捷
4. 支持PEP8代码规范检测
5. git日志内容支持友好地阅读
6. 自带`python Console` 和`terminal` 「win下则是cmd」
7. 自带快速查询手册

> [msysgit官网](https://git-for-windows.github.io)
>
> [Pycharm官网说明](http://www.jetbrains.com/pycharm/documentation/)

