# 简介

一个简易的企业微信机器人框架

用于构建一个可以进行对话交互的企业微信机器人

特性：

- 正则匹配和关键词匹配，两种方式进行消息识别，精准回复消息
- 会话日志输出，运行过程中的机器人对话全程记录
- 简单的参数配置即可运行，轻量便携

# 使用说明

## 配置环境

命令行下执行以下指令

```shell
git clone https://github.com/Biubush/WechatWorkBot.git # 拉取仓库到本地
cd WechatWorkBot # 进入文件夹
pip install -r requirements.txt # 安装依赖库
```

## 配置参数

### CORP_ID获取

首先打开[企业微信](https://work.weixin.qq.com/wework_admin/frame)，点击导航栏的**我的企业**

然后将页面最底端的**企业ID**复制下来，粘贴到项目文件夹下的**config.py**中的**CORP_ID**中（记得有英文双引号）

### AGENT_ID和CORP_SECRET获取

在[企业微信](https://work.weixin.qq.com/wework_admin/frame)导航栏的**应用管理**中在**自建**板块点击**创建应用**

配置完毕进入应用管理页面后，将**AgentId**复制粘贴到项目文件夹下的**config.py**中的**AGENT_ID**中（记得有英文双引号）

点击**Secret**下的查看，去手机上的企业微信中查看Secret，复制粘贴到项目文件夹下的**config.py**中的**CORP_SECRET**中（记得有英文双引号）

### TOKEN和ENCODING_AES_KEY获取

在上一步打开的应用管理页面中，找到功能-接收消息-设置API接收

> 注意，以下为重点步骤

输入URL内容应为http://<你的公网ip>:44722/api/wechat

如果你部署了域名，请根据实际情况进行更改

然后，在该页面自定义或随机生成Token和EncodingAESKey，分别复制粘贴到项目文件夹下的**config.py**中的**TOKEN**和**ENCODING_AES_KEY**中（记得有英文双引号）

注意，保持这个网页页面不要操作，后续运行起服务再进行下一步

### 额外参数

有以下额外参数可以添加进项目文件夹下的**config.py**中，但这些是非必要的

- WORK_DIR # 工作文件夹，日志依赖此参数生成
- SECRET_KEY # flask的秘钥对，有需要可以自行定义
- DEBUG # flask是否以debug模式运行，布尔值，填Ture或False
- PORT # 项目运行端口，整型

## 配置对话规则

编辑**WechatWorkBot\msg_handler.py**，有两种匹配对话的方式

1. 正则匹配

2. 关键词匹配

正则匹配使用@re_method装饰器，传入一个正则表达式，当用户发送的消息匹配该正则表达式时，将调用该函数处理消息

关键词匹配使用@contain_method装饰器，传入一个字符串，当用户发送的消息包含该字符串时，将调用该函数处理消息

## 运行项目

执行以下命令

```
python run.py
```

即可运行起项目

此时在**API接收消息**的页面点击**保存**，稍作等待即可配置完成

再返回你的应用配置页面，找到**开发者接口**-**企业可信IP**-**配置**，将你的服务器ip填入并保存

至此，你的项目理论上可以正常运行

# 报错说明

在运行过程中有报错时，请按照程序给你的指示进行排查和修复