# pymirai

___中文代码警告___

__【注意】务必使用新版本的 mirai-api-http >= \(1.6.0)__

来自[mirai_http_python](https://github.com/super1207/mirai_http_python)  
不知道改了多少, 目前版本的mirai-console能用就是了  
啰唆一句, 是 AGPL

使用的时候先要成功启动[mirai-console](https://github.com/mamoe/mirai-console)，并正确加载[mirai-api-http](https://github.com/mamoe/mirai-api-http)，这两个项目里写得很详细了，跑不起来雨我无瓜

虽然是傻叉风格的中文代码但是不懂编程真的是跑不起来的！！！

DEMO：

```python
#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from pymirai import BOT

class info:
    host = "http://localhost:8080"
    botqq = bot的QQ
    botkey = "mirai api http 的key"
    adminqq = 你的QQ


##############################################################################


def 格式化消息链(msg, quote = False): #（这个格式化消息链真香）
    """返回成一般可读形式，并触发被at"""
    msg_formatted=""
    for i in msg['messageChain']:
        if i["type"] == "Plain":
            msg_formatted += i["text"]
        elif i["type"] == "Face":
            msg_formatted += "[face: " + i["name"] + "]"
        elif i["type"] == "Image":
            msg_formatted += "[图片:"+i["imageId"]+"]"
        elif quote == False:
            if i["type"] == "Quote":
                msg_formatted += ("[回复" + str(i["senderId"]) + "]")
                #msg_formatted += ("[回复" + str(i["senderId"]) + ": " + 格式化消息链(i["origin"], True) + "]")
            elif i["type"] == "At":
                msg_formatted += i["display"]
                if i["target"] == info.botqq:
                    At事件(msg)
    return msg_formatted


#######################################################################

def At事件(msg):
    群号 = msg['sender']['group']['id']
    群员号 = msg['sender']['id']

    def 说(消息):
        机器人.发消息给群(群号, [{"type": "Plain", "text": 消息}, ])

    说("at我干什么")


def 群组消息(bot, msg):

    群号 = msg['sender']['group']['id']
    群员号 = msg['sender']['id']

    内容 = 格式化消息链(msg)

    def 说(消息):
        机器人.发消息给群(群号, [{"type": "Plain", "text": 消息}, ])

    if (内容 == "你好"):
        说("你好")


#######################################################################

def 好友事件(bot, msg):
    usr_id = msg['sender']['id']
    if usr_id == info.adminqq:
        机器人.发消息给好友(usr_id, [{"type": "Plain", "text": "你是管理员"},])
    else:
        机器人.发消息给好友(usr_id,[{"type": "Plain", "text": "你是好友"}, ])


#######################################################################
if __name__ == "__main__":
    机器人 = BOT(info.host, info.botqq, info.botkey)
    机器人.新增事件("FriendMessage", 好友事件)
    机器人.新增事件("GroupMessage", 群组消息)
    print("Connecting")
    if 机器人.连接():
        print("Connected")
        机器人.发消息给好友(info.adminqq, [{"type": "Plain", "text": "Hello World"}, ])
        机器人.等()
        机器人.断开()
```
写了个`登录(密码)`，但是鉴于现在的mirai-console的特性用不了。