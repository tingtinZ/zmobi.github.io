---
layout: post
title: VyprVPN在dd wrt中的设置
description: 在dd wrt系统中设置VyprVPN翻墙上网，使用OpenVPN的方式
category: 路由器
keywords: dd wrt, VyprVPN, OpenVPN, 翻墙
---

刷完路由器之后，首当其冲的任务是设置VPN翻墙，理想状态是家里任何设备只要连接上路由器，即可无痛浏览国外网站，解除**功夫网**的限制。经过我大谷歌的搜索，在往后的几页当中发现了一个国外友人共享的教程，成功生效，接下来详细讲解操作步骤。

<!-- more -->

## 静态DNS设置

登录管理界面后，在 *设置* => *基本设置* 中修改静态DNS的地址，使用开源的DNS—— [OpenDNS](https://www.opendns.com/welcome/) ，干净无污染。这点很重要噢亲。

```txt
Static DNS 1: 208.67.222.222
Static DNS 2: 208.67.220.220
```

## VPN设置

在 *服务* => *VPN* 中，设置*VyprVPN* 的相关选项，启用`OpenVPN客户端`, 填写信息如下：

```txt
Server IP/name: 填写VyprVPN的各地区域名
Port: 1194
Tunnel Device: TUN
Tunnel Protocol: UDP
Encryption Cipher: Blowfish CBC
Hash Algorithm: SHA1
User Pass Authentication: Enable
Username: 你的VyprVPN账号
Password: 你的VyprVPN密码
Advanced options: Enable
TLS Cypher: None
LZO Compression: Yes
NAT: Enable
Firewall Protection: Enable
```

*Additional Config* 填写

```txt
resolv-retry infinite
keepalive 10 60
nobind
persist-key
persist-tun
persist-remote-ip
verb 3 
```

下载[CA证书](https://support.goldenfrog.com/hc/en-us/article_attachments/201553633/CA_Cert.txt) ，并粘贴到 **CA Cert** 对话框中

接着 *保存设置* 并 *应用* 之使其生效，之后到 `状态` 标签下，会多出一个**OpenVPN** 副标签，点击查看VPN连接情况

## 存在问题

路由器内所有设备走的都是VPN通道，我选的是香港，因此浏览器访问天朝购物网站如淘宝之类的，会默认显示为国际版。解决方法是在路由器中添加自动分流处理，让墙外的均走VPN通道，墙内的直接走的本地。暂时还未能处理先，晚点再解决吧。

实测OpenVPN的连接确实很稳定，香港线路访问天朝网站的速度还可以让人接受噢。

> [外国友人的原文](https://tomssl.com/2015/06/01/install-vyprvpn-on-your-dd-wrt-router-to-encrypt-all-of-your-internet-traffic/)
