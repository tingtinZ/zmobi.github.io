---
layout: post
categories: Linux
description: ZSH在UBUNTU上的配置 
title: linux上布署ZSH脚本
keywords: zsh, ubuntu
---


误打误撞地在`MacTalk`的知乎专栏上看到有关`ZSH`的简单使用与配置教程，考虑到要适配自己的环境，并且懒得每次搜索，本着懒惰的性格，呵呵，遂在此记录下来，以便备用时直接*copy*代码在机器上跑一次即可

<!-- more -->

```shell
#! /bin/bash

# 安装zsh
sudo apt-get install zsh

# 安装Git
[ -f /usr/bin/git ] || sudo apt-get install git

# 安装autojump
sudo apt-get install python-pip pip setuptools
wget https://github.com/downloads/joelthelion/autojump/autojump_v21.1.2.tar.gz
tar -xf autojump_v21.1.2.tar.gz
cd autojump_v21.1.2
./install.sh

# 安装oh-my-zsh
sudo apt-get install curl wget
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

# 修改.zshrc配置
sed -i '/ZSH_THEME/ s/robbyrussell/candy-kingdom/' ~/.zshrc
echo '[[ -s /etc/profile.d/autojump.zsh ]] && . /etc/profile.d/autojump.zsh' >> ~/.zshrc
```
