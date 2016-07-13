### RTX 以HTTP方式发送RTX提醒

- 安装`RTX`的`sdk` 

在rtx服务端所在机器上安装rtx的sdk，或者直接完整安装RTX服务端即可。在安装的根目录上使用*notepad++*打开文件`SDKProperty.xml`，按照以下格式修改

```xml
<?xml version="1.0"?>
<Property>
<APIClient>
	<IPLimit Enabled="1">
		<IP>127.0.0.1</IP>
         <!-- 我是新添加的IP -->
		<IP>10.0.0.122</IP>
	</IPLimit>
</APIClient>
<sdkhttp>
    <!-- 将原有值1改成0 -->
	<IPLimit Enabled="0">
	</IPLimit>
</sdkhttp>
</Property>
```

如果有多个IP地址，则所有都需要添加上！

- 开启服务

按`win+r`键，输入 **services.msc** ，重启这两个服务：`RTX_HTTPServer`和`RTX_SvrMain`

> 当初折腾时，网上的文章完全没人提到这两个服务，心好累，特别是RTX_HTTPServer没开启，无法使用8012这个端口

- 测试消息

在添加IP所在的主机「*此处为10.0.0.122*」，浏览器中访问：

`http://rtx_server_ip:8012/SendNotify.cgi?msg=hello&receiver=test`，此时电脑右下角会有消息弹窗