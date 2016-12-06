---
layout: post
title: 科学上网之shadowsocks
description: 在Ubuntu中搭建shadowsocks服务器，并在各种客户端上的具体使用
category: 效率
keywords: shadowsocks, ss, 科学上网

---

终于狠心买了台VPS来玩玩，想搭个博客网站，顺便弄个自己的GIT，以及把科学上网的问题也解决了，算是一举多得吧……在网站还未正式弄完的时间里，不能把服务器闲着，于是乎顺带把`shadowsocks` 给了解一番。

<!-- more -->

# Shadowsocks服务端

## 安装

VPS服务器我选的是 *ubuntu* ，平时也在用，怎么熟手怎么来吧。

```shell
# 借助的是python来具体实现的
sudo apt update
sudo apt install python-pip
sudo pip install easy_setuptools
sudo pip install shadowsocks
sudo apt install python-m2crypto
```

## 运行

单条命令执行

```shell
sudo ssserver -p 8388 -k password -m rc4-md5 -d start
```

建议最好是写在配置文件里头启动会更方便些

```shell
# /etc/shadowsocks.json
{
    "server":"my_server_ip",
    "server_port":8388,
    "local_address": "127.0.0.1",
    "local_port":1080,
    "password":"mypassword",
    "timeout":300,
    "method":"rc4-md5"
}
```

加密方式推荐使用rc4-md5，因为 RC4 比 AES 速度快好几倍，如果用在路由器上会带来显著性能提升。旧的 RC4 加密之所以不安全是因为 Shadowsocks 在每个连接上重复使用 key，没有使用 IV。现在已经重新正确实现，可以放心使用。

如果需要配置多个用户，可以这样设置

```shell
{
    "server":"my_server_ip",
    "port_password": {
        "端口1": "密码1",
        "端口2": "密码2"
    },
    "timeout":300,
    "method":"rc4-md5",
    "fast_open": false
}
```

## 开机启动

写入到开机启动的配置文件

```shell
# 使用配置文件的启动
sudo echo '/usr/local/bin/ssserver –c /etc/shadowsocks.json' >> /etc/rc.local

# 单条命令的启动
sudo echo '	/usr/local/bin/ssserver -p 8388 \
-k password -m aes-256-cfb -d start' \
>> /etc/rc.local
```

## 内核参数修改之网络优化

主要是修改两个文件

- /etc/sysctl.conf
- /etc/security/limits.conf

```shell
sudo cat >> /etc/sysctl.conf << EOF
# max open files
fs.file-max = 51200
# max read buffer
net.core.rmem_max = 67108864
# max write buffer
net.core.wmem_max = 67108864
# default read buffer
net.core.rmem_default = 65536
# default write buffer
net.core.wmem_default = 65536
# max processor input queue
net.core.netdev_max_backlog = 4096
# max backlog
net.core.somaxconn = 4096
# resist SYN flood attacks
net.ipv4.tcp_syncookies = 1
# reuse timewait sockets when safe
net.ipv4.tcp_tw_reuse = 1
# turn off fast timewait sockets recycling
net.ipv4.tcp_tw_recycle = 0
# short FIN timeout
net.ipv4.tcp_fin_timeout = 30
# short keepalive time
net.ipv4.tcp_keepalive_time = 1200
# outbound port range
net.ipv4.ip_local_port_range = 10000 65000
# max SYN backlog
net.ipv4.tcp_max_syn_backlog = 4096
# max timewait sockets held by system simultaneously
net.ipv4.tcp_max_tw_buckets = 5000
# turn on TCP Fast Open on both client and server side
net.ipv4.tcp_fastopen = 3
# TCP receive buffer
net.ipv4.tcp_rmem = 4096 87380 67108864
# TCP write buffer
net.ipv4.tcp_wmem = 4096 65536 67108864
# turn on path MTU discovery
net.ipv4.tcp_mtu_probing = 1
# for high-latency network 
net.ipv4.tcp_congestion_control = hybla
# for low-latency network, use cubic instead
#net.ipv4.tcp_congestion_control = cubic
EOF

# 开启hybla算法
/sbin/modprobe tcp_hybla

# 令参数生效
sudo sysctl -p

# 增加文件大小限制
cat >> /etc/security/limits.conf << EOF
* soft nofile 51200
* hard nofile 51200
EOF

ulimit -n 51200
```

设置完成后，重启 *shadowsocks* 服务即可。

如果想要观看 *youtube 1080p* 视频的话，*cubic*仅最高支持 *720p*。

```shell
# 必须选hybla算法
net.ipv4.tcp_congestion_control = hybla
```

查看系统当前支持的算法有哪些

```shell
# 执行
sudo sysctl net.ipv4.tcp_available_congestion_control
```

返回的结果中，如果有 *hybla* ，则证明支持该算法；否则，只能将就着看 *720p*的吧。

# 客户端使用

客户端 *ubuntu* 使用时则非常简单，设置同样的配置文件`/etc/shadowsocks.json` ，前提要安装的软件也给装上，两边的配置文件要一致噢。区别是启动的命令不同

```shell
sslocal -c /etc/shadowsocks.json
```

当然也可以是单条命令的。

这种方式是前端执行命令，必须得占用一个 *terminal* 窗口，略为麻烦，因此可以借助另一个工具来实现后台运行。

```shell
# 安装软件
sudo apt-get install supervisor

# 创建配置文件 
sudo cat > /etc/supervisor/conf.d/ss.conf << EOF
[program:shadowsocks]
command=sslocal -c /home/your_user_name/shadowsocks.json
autostart=true
autorestart=true
user=your_user_name
log_stderr=true
logfile=/var/log/shadowsocks.log
EOF

# 借助supervisor管理
/etc/init.d/supervisor restart
```

# 浏览器设置

当客户端开启了 *ss* ，想要科学上网，必须得在浏览器在设置代理。显然，*ss* 是无法做全局使用，好处是科学上网体验很舒服，墙内墙外都如丝般顺滑。如果全局都走代理，像我原本连接着的服务器，则自动帮你断开，蛋疼得一逼。目前要实现自动切换代理的，仅是 *chrome* 浏览器。

首先是下载插件： [https://github.com/FelisCatus/SwitchyOmega/releases/](https://github.com/FelisCatus/SwitchyOmega/releases/) 

然后在*chrome* 地址栏中打开： chrome://extensions/，把下载好的插件拖进去安装即可。

插件安装完毕后，它会有教程提醒你，可以点击跳过。

设置步骤：

`新建情景模式` ： 名称随便，如 SS，选择 *代理服务器*

`设置SS`： 网址协议选默认，代理协议选 *socks5* ，代理服务器写 *127.0.0.1* ，代理端口写 *1080*

点击保存后。

`auto switch` ： 选择*autoproxy*，规则列表网址写这个 
https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt 。
默认情景模式选择 直接连接，规则列表规则 的情景模式则选 SS即可。

详细的图文设置， [请猛击我](https://aitanlu.com/ubuntu-shadowsocks-ke-hu-duan-pei-zhi.html)

# 尾巴

关于加密算法这块，我还特意找了好些文章来学习，原来还有新的 *chacha20* 算法，ss默认推荐的算法是 *aes-256-cfb* ，对 *rc4-md5* 算法普遍认为安全性太差，虽然效率上比较占优势。我在 *ea6300 v1* 路由器上，选择了默认算法，也没见效率有多低，待我有空测测观看 *youtube 1080p* 视频时看看如何。

暂时还未在 *windows* 装客户端，平时很少用；*android* 的亦是如此。*IOS* 上推荐 `Wingy`，免费的噢，效果杠杠的。
