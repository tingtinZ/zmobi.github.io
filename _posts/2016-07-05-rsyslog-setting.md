---
layout: post
categories: Linux
description: 使用rsyslog记录bash的操作日志
title: Rsyslog记录用户的所有命令
keywords: rsyslog, linux
---


本文承接文章**多人使用同一系统用户的操作记录**的后续操作，当/var/log/message中可以记录用户的详细操作命令后，假如某个用户执行错误或者非法命令，企图删除message当中的记录时，这尼玛岂不是要上天了？遂需要将message的日志记录实时同步到日志服务器里，集中管理日志，方便查询，让坏人无处躲藏。

背景需知：CentOS 6系列的系统，已经默认安装了rsyslog，用其取代旧有的syslog
<!-- more -->

```shell
## 日志服务端  10.0.0.220
## 日志客户端  10.0.0.222

# 查询rsyslog版本
rsyslogd -v
# 默认安装的是5.8.10版，此处升级成8的版本
cat > /etc/yum.repos.d/CentOS-Other.repo << EOF
[rsyslog-v8-stable]
name=Adiscon Rsyslog v8-stable for CentOS-\$releasever-\$basearch
baseurl=http://rpms.adiscon.com/v8-stable/epel-\$releasever/\$basearch
enabled=1
gpgcheck=0
protect=1
EOF

# 安装v8版本的rsyslog
yum clean all
yum makecache
yum -y update rsyslog

## 同步所有message的日志

# 服务端配置 10.0.0.220
cat > /etc/rsyslog.conf <<EOF
# Server
global(net.enableDNS = "on")
global(net.ipprotocol = "ipv4-only")
global(debug.onShutdown = "on")
\$maxMessageSize      16K
\$AllowedSender       TCP
module(load="imuxsock") # provides support for local system logging (e.g. via logger command)
module(load="imklog")   # provides kernel logging support (previously done by rklogd)
module(load="imtcp") # needs to be done just once
input(type="imtcp" name="10.0.0.222" port="514")
\$ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat
\$IncludeConfig /etc/rsyslog.d/*.conf
# template定义服务端接收到客户端的日志后，存放路径与文件名
# %hostname%表示客户端的主机名，需在客户端的/etc/hosts设置，下面会讲到
# %fromhost-ip%表示客户端的IP
template(name="remote_syslog" type="string" string="/var/log/rsyslog_center/%hostname%_%fromhost-ip%/%\$YEAR%-%\$MONTH%/%\$DAY%/%PROGRAMNAME%.log")

kern.*                                                  /var/log/kernel
*.info;mail.none;authpriv.none;cron.none                /var/log/messages
auth.*;authpriv.*                                       /var/log/secure
mail.*                                                  /var/log/maillog
cron.*                                                  /var/log/cron
daemon.*                                                /var/log/daemon
user.*                                                  /var/log/user
*.emerg                                                 :omusrmsg:*
uucp,news.crit                                          /var/log/spooler
local7.*                                                /var/log/boot
*.*                                                     ?remote_syslog
EOF

# 客户端配置 10.0.0.222
cat > /etc/rsyslog.conf <<EOF
#Client
global(net.enableDNS = "on")
global(net.ipprotocol = "ipv4-only")
global(debug.onShutdown = "on")
\$maxMessageSize      16K
module(load="imuxsock") # provides support for local system logging (e.g. via logger command)
module(load="imklog")   # provides kernel logging support (previously done by rklogd)
\$ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat
\$IncludeConfig /etc/rsyslog.d/*.conf
kern.*                                                  /var/log/kern
*.info;mail.none;authpriv.none;cron.none                /var/log/messages
auth.*                                                  /var/log/auth
authpriv.*                                              /var/log/secure
mail.*                                                  /var/log/maillog
cron.*                                                  /var/log/cron
daemon.*                                                /var/log/daemon
user.*                                                  /var/log/user
*.emerg                                                 ~
uucp,news.crit                                          /var/log/spooler
local7.*                                                /var/log/boot
*.*                                                     @@10.0.0.222:514
EOF

## 修改配置的后续操作
chkconfig rsyslog on
chkconfig --list rsyslog
# 快速检测rsyslog配置有无问题
rsyslogd -f /etc/rsyslog.conf -N1
/etc/init.d/rsyslog restart
# 服务端的/etc/sysconfig/rsyslog，记得要留空，否则无法重启rsyslog
SYSLOGD_OPTIONS=""
# 客户端的/etc/hosts，获取本机HOSTNAME后，添加到第一行； 这样在服务端方能查询到是哪台主机，哪个IP的历史命令
127.0.0.1 Your_HostName
# 防火墙添加放行相应的端口，区分tcp与udp
-A RH-Firewall-1-INPUT -p tcp -m state --state NEW -m tcp --dport 514 -j ACCEPT
```

#### 挑选SSH操作日志

假如我只想要用户执行命令的历史记录，那又该如何设置呢？

```shell
## Client /etc/rsyslog.confg配置
# 把上述客户端配置的最后一行按如下修改
# :rawmsg,contains,"bash" 代表 仅保留历史记录是bash的部分

#*.*			@@10.0.0.222:514
:rawmsg,contains,"CMD"		@@10.0.0.222:514    




## Server /etc/rsyslog.confg配置
# 原有的下列两行需注释掉
#template(name="remote_syslog" type="string" string="/var/log/rsyslog_center/%hostname%_%fromhost-ip%/%$YEAR%-%$MONTH%/%$DAY%/%PROGRAMNAME%.log")
#*.*                                                     ?remote_syslog

# 在template(name="remote_syslog" ..... 这行下添加
# 定义一个名为logformat模板, 为信息加上日志时间
$template logformat,"%TIMESTAMP% %hostname% %FROMHOST-IP%%msg%\n" # 定义日志文件的名称，按照年月日    
$template DynFile,"/var/log/rsyslog_center/%hostname%_%fromhost-ip%/SSH_CMD_%$YEAR%-%$MONTH%-%$DAY%.log"  
# 把rawmsg(也可以使用msg)日志中包含CMD标志的信息写到DynFile定义的日志文件里
:rawmsg, contains, "CMD" ?DynFile;logformat    
```



#### rsyslog 2.5.8版本

主要是服务端的小小变化而已

```shell
# 服务端配置 10.0.0.220
cat > /etc/rsyslog.conf <<EOF
# Server

\$ModLoad imtcp.so              # needs to be done just once #使用tcp方式
\$InputTCPMaxSessions 500    # tcp接收连接数为500个
\$InputTCPServerRun 514      # tcp接收信息的端口
\$ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat
\$IncludeConfig /etc/rsyslog.d/*.conf
\$template logformat,"%TIMESTAMP% %hostname% %FROMHOST-IP%%msg%\n"
\$template DynFile,"/var/log/rsyslog_center/%hostname%_%fromhost-ip%/SSH_CMD_%\$YEAR%-%\$MONTH%-%\$DAY%.log" 
:rawmsg, contains, "CMD" ?DynFile;logformat  

kern.*                                                  /var/log/kernel
*.info;mail.none;authpriv.none;cron.none                /var/log/messages
auth.*;authpriv.*                                       /var/log/secure
mail.*                                                  /var/log/maillog
cron.*                                                  /var/log/cron
daemon.*                                                /var/log/daemon
user.*                                                  /var/log/user
*.emerg                                                 :omusrmsg:*
uucp,news.crit                                          /var/log/spooler
local7.*                                                /var/log/boot
EOF
```

**参考文献**

> [Rsyslog Server V8](http://my.oschina.net/guol/blog/674442?fromerr=DZSo5W6a)
>
> [Rsyslog配置文件详解](http://my.oschina.net/0757/blog/198329)

