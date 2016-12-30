---
layout: post
title: rsync的使用小结
description: rsync使用小结
category: Linux
keywords: linux, rsync
---

主要分为服务端与客户端，服务端主要是用来存储需要备份的数据，客户端则为主动提供需要备份的数据，交给服务端。

<!-- more -->

**rsync server**端主要设定下列3个选项

- 规划建立备份的目录

- 设定主要配置文件： /etc/rsyncd.conf

- 设定密码文件： /etc/rsyncd.secrets

  ```shell
  ## 设定主要的配置文件
  cat > /etc/rsyncd.conf << EOF
  log file = /var/log/rsyncd.log
   #设定备份目录的区块，不同的备份任务建立不同的区块即可
  [Jeff_Block]
  	path = /tmp/backup
  	auth users = jeff
  	uid = root
  	gid = root 
  	secrets file = /etc/rsyncd.secrets
  	read only = no
  EOF

  ## 设定密码文件
  echo 'user:passwd' > /etc/rsyncd.secrets # 此处仅为范例而已
  chown root:root /etc/rsyncd.secrets
  chmod 600 /etc/rsyncd.secrets

  ## 启动rsyncd服务，如果是使用守护进程启动的话
  /etc/init.d/rsync start 

  ## 检查下Iptable与netstat，注意873端口
  ## 相关的日志记录均在 /var/log/rysncd.log
  ```

**rsync client**端的主要设定

- 设定密码文件
- 测试rsync执行命令
- 将rsync指令加入到crontab计划任务中

此处就不重复该步骤了，跳过

#### 安全性

- 如果使用rsync daemon模式，建议在rsync server中使用Iptables指令来限制rsync client的连接范围，如

```shell
iptables -A INPUT -p tcp -s ! 11.22.33.44 --dport 873 -j DROP
```

只有上述IP才能连接这台SERVER端，但批量设定比较麻烦

- 鉴于提升安全性，可使用**rsync**与**openssh**搭配使用

```shell
## rsync选项-e 调用ssh来做连接加密的操作
rsync -avHS -e ssh /root/tmp root@hostname:/root
```

#### 使用rsync+ssh同步备份文件

```shell
## 备份服务器 192.168.200.134
## 目标服务器 192.168.201.65

# 主要用到的同步命令是
rsync -avzHS -e 'ssh -p <端口，默认是22>' <本地待备份的目录> 目标IP:<目标目录> 

# 免密码登录的方式同步
# 在备份服务器上生成密钥 ssh-keygen -t rsa,生成ssh rsa私钥 id_rsa  和公钥id_rsa.pub
# 然后把公钥同步到目标服务器相应存储公钥的目录\
# 最后在目标服务器上添加计划任务，以命令或者脚本的形式均可
crontab -e
rsync -avzHS -e 'ssh -p <端口，默认是22>' <本地待备份的目录> 目标IP:<目标目录> > /dev/null 2>&1
## 建议以脚本的形式会比较好，可自定义传输日志
```

#### rsync命令参数详解

下列仅摘抄部分使用率较广的命令

```shell
# 把111目录以及目录下所有文件同步到tmp的322下
rsync -av 111/  /tmp/322/

# --delete 删除源端中没有的文件
rsync -avL --delete 111/  /tmp/322/ 

#  -u不删除和源文件中不一样的文件
rsync -avLu 111/ /tmp/322/

# 源文件中的23不会备份过去。可以通配--exclude=“*.txt”
rsync -avLu 111/ --exclude=“23” /tmp/322/ 

# 只复制目录结构，忽略掉文件
rsync -av --include '*/' --exclude '*' source-dir dest-dir

# 先备份，再同步
rsync -ab –-backup-dir=/data/backup/指定目录 –-suffix=后缀 ./ /tmp/django/
# -b代表先备份，再同步
# -–backup-dir=/data/backup/指定目录，如果目录不存在，rsync会自动创建目录
# -–suffix=后缀指定备份文件名的后缀
# 只有当目标文件与待推送文件不同时，备份机制才生效
```

#### Rsync计划任务的中备份脚本

```shell
#! /bin/bash 

## 注意请区别推与拉的方式

log_file='/var/log/rsyncd_log'
IP='10.0.0.220'

Start_Time=$(date +"%Y-%m-%d_%H:%M:%S")

echo '' >> ${log_file}
echo "rsync start ${Start_Time} ${IP}"  >> ${log_file}
#rsync -avrHS -e 'ssh -p 51518'  /usr/local/src/src_tar/  ${IP}:/tmp/test_rsync/ >& ${log_file}
rsync -avrHS -e 'ssh -p 22'  ${IP}:/usr/local/src/src_tar/  /tmp/test_rsync/ >> ${log_file} 2>&1

Stop_Time=$(date +"%Y-%m-%d_%H:%M:%S")
echo "rsync stop ${Stop_Time} ${IP}"  >> ${log_file}
```

## Rsync多个目录同步

```shell
# 方式一: 写多次咯
rsync -avh --exclude=xxx --exclude=xxx ip:/sou_dir des_dir

# 方式二：写到一个文件
rsync -avh --exclude-from='exclude.list' sou_dir des_dir
## exclude.list 文件内容为：
dir1
dir2
dir3
.dir4

# 方式三：用{}
rsync -avh --exclude={dir1,dir2} sou_dir des_dir
```



> 参考1 ：[rsync详解网友资料](http://www.cnblogs.com/itech/archive/2009/08/10/1542945.html)
>
> 参考2 ：[rsync详解与后台方式运行](http://www.mamicode.com/info-detail-1242643.html)

