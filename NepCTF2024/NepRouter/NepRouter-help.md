1.获取题目端口，改写链接格式

```
neptune-xxx.nepctf.lemonprefect.cn

如:neptune-27607.nepctf.lemonprefect.cn
```

2.下载stunnel

```
https://www.stunnel.org/downloads.html
```

3.配置代理规则

```
用管理员权限启动stunnel
右键托盘中的图标，点击编辑配置文件，在末尾插入如下内容，端口以实际为准

; TLS-encrypted SOCKS5 Proxy
[socks5-tls]
client = yes
accept = 127.0.0.1:1081
connect = neptune-xxx.nepctf.lemonprefect.cn:443
```

4.启动stunnel

```
右键托盘中的图标，点击重载配置文件后点击连接
```

5.下载Proxifier

6.配置代理服务器

```
代理服务器地址为127.0.0.1
端口1081
协议socks5，开启认证
用户名：proxyUser
密码：123456
```

7.访问题目入口

```
http://127.0.0.1:5000/
```

Tips：

```
除了stunnel与Proxifier，请关闭其他的代理软件
```

