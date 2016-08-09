---
layout: post
category: Linux
title: ubuntu当工作机使用
description: 使用ubuntu当工作机，日常使用时所需做的配置
keywords: ubuntu, 工作机, 日常使用, 开发使用
---

因工作原因，不想把时间浪费在折腾`瘟到死`系统配置的死循环中，想弄个Mac过来装逼，但奉行够(que)用(shi)就(mei)好(qian)的原则，遂把工作机换成了*ubuntu*系统。以安装双系统的方式共存，安装方法之前的文章已经有说过了。接着是理清下思路，切换工作环境，需要做哪些准备，是否影响日常的工作呢？
<!-- more -->

### 友情提示
 .deb包无法直接在图形界面安装，使用命令安装
 
```shell
 dpkg -i your_package_name.deb
 # 部分软件缺少信赖关系，系统会提示你解决方法
 sudo apt -f install
```

### 远程
1. teamviewer支持linux版本
2. ubuntu系统自带 remmina远程桌面客户端，支持访问windows系统

### VPN翻墙
实测自购的VPN，以PPTP方式登录正常

### linux机器管理
SecureCRT居然有了linux版本，啧啧。

```shell
# 到官网下载ubuntu版本的CRT
# 下载破解程序
wget http://download.boll.me/securecrt_linux_crack.pl  
# 执行破解，生成注册信息
sudo perl securecrt_linux_crack.pl /usr/bin/SecureCRT  
# 接着按windows的步骤填写信息即可
```

### 文档处理
暂时使用自带的LibreOffice，如果实在不好用，再考虑换wps for linux吧

### 密码管理keepass
中文字体显示异常，但不影响日常使用

```shell
sudo apt-add-repository ppa:jtaylor/keepass
sudo apt-get update
sudo apt-get install keepass2
```

### 坚果云同步
下载deb包，执行`dpkg -i`安装即可

###  Pycharm

```shell
# 官网下载压缩包
mv pycharm-community-2016.2.tar.gz /opt
cd /opt && tar -xf pycharm-community-2016.2.tar.gz
sudo ln -s /opt/pycharm-community-2016.2/bin/pycharm.sh /usr/bin/pycharm
```

### sublime text2
安装这货真心折腾啊，重点要解决中文输入法的问题

```shell
sudo add-apt-repository ppa:webupd8team/sublime-text-2
sudo apt update
sudo apt install sublime-text
# 解决中文输入的问题
cd /tmp 
git clone https://github.com/lyfeyaj/sublime-text-imfix.git
cd sublime-text-imfix 
# 我用的是2，默认的是3，因此做小小修改
sed -i 's/sublime_text/sublime_text2/g' sublime-imfix
sed -i 's/sublime_text/sublime_text2/g' src/subl
./sublime-imfix
# 执行完毕后，会解锁一个我之前很喜欢的QQ五笔皮肤
```

### QQ与RTX
这两个货暂时无解，网上应该有wine方式的安装，暂时不想折腾，于是装个virutalbox虚拟机，装个WIN7，就挂着QQ和RTX。没办法啊，工作要用RTX。

## 尾巴

把上述东东折腾完毕，想着听首歌放松下，立马打开浏览器访问网易云音乐，可惜没装flash，无法在线播放，查看其客户端种类，OMG，居然支持Linux了，啧啧。
对比三四年前实体机安装ubuntu的体验，明显有很大的进步啊。使用linux的人群似乎增多了，很多软件逐步支持linux了，如secureCRT、网易云音乐等等，鹅厂的除外。ubuntu使用体验完全不输于windows，对于开发者而言，ubuntu可能是上不了mac， 下不想win的折衷解决方案了。

