# 文件共享系统GUI

## 目录介绍

<img src="https://hanshansite-1307452666.cos.ap-shanghai.myqcloud.com/site-img/截屏2022-11-04 16.57.28.png"/>

*   file1和file2为测试目录，供节点服务器启动时作为工作目录
*   center_server.py为中心服务器文件
*   guiclient.py为GUI客户端文件
*   node_server为节点服务器文件
*   REDEME.md为项目说明文件
*   requirements.txt为项目所必须包文件（该项目可以在原生python下运行）

## 运行环境搭建

本项目可以在原生python下运行，不需要安装第三方包

## 运行指令
### 运行中心服务器

```
python center_server.py [中心服务器url]
# 示例
python center_server.py http://localhost:11000
```

### 运行GUI客户端

```shell
python guiclient.py [本地节点的url] [本地节点工作目录]
# 示例
python guiclient.py http://localhost:13000 ./file2
python guiclient.py http://localhost:12000 ./file1
```

**注意：不需要单独运行node_server.py文件，该文件会在guiclient.py中自动启动**



