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

### SSH-KEY 密码管理

本机上的**SSH-Key** 管理 ，特指key有密码的情况，方法有两种，均是在*.bashrc* 或者 *.zshrc* 中操作

```shell
# 方法一
apt install keychain
eval `keychain --eval id_rsa`

# 方法二
eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_rsa
```

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
中文字体显示异常，安装完毕之后，需要进入软件设置，选择google的开源字体: `思源体 - noto sans`

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

### Typora

從來不看更新日志的在下，某次心血來潮掃了一下，不得了啊～**Typora** 居然支持 *linux* 了，老子那個激動啊。個人比較喜歡的一款 *markdown* 軟件，三打操作系統平臺均支持。

```shell
# 額外的選項，但強烈建議添加
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys BA300B7755AFCFAE

# 添加軟件源
sudo add-apt-repository 'deb https://typora.io linux/'
sudo apt-get update

# 安裝 typora
sudo apt-get install typora
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
# 执行完毕后，会解锁一个我之前很喜欢的QQ五笔皮肤
./sublime-imfix
# sublime用户自定义配置
{
    "font_face": "Ubuntu Mono",
    "font_size": 16,
    "highlight_line": true,
    "tab_size": 4,
    "translate_tabs_to_spaces": true,
    "word_wrap": true
}
```

### QQ与RTX
~~这两个货暂时无解，网上应该有wine方式的安装，暂时不想折腾，于是装个virutalbox虚拟机，装个WIN7，就挂着QQ和RTX。没办法啊，工作要用RTX。~~

参考[ubuntu安装qq与rtx]({{ site.url }}/2016/11/09/ubuntu-install-qq-and-rtx)

## 尾巴

把上述东东折腾完毕，想着听首歌放松下，立马打开浏览器访问网易云音乐，可惜没装flash，无法在线播放，查看其客户端种类，OMG，居然支持Linux了，啧啧。
对比三四年前实体机安装ubuntu的体验，明显有很大的进步啊。使用linux的人群似乎增多了，很多软件逐步支持linux了，如secureCRT、网易云音乐等等，鹅厂的除外。ubuntu使用体验完全不输于windows，对于开发者而言，ubuntu可能是上不了mac， 下不想win的折衷解决方案了。

