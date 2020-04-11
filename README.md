# pymirai

中文代码警告

来自[mirai_http_python](https://github.com/super1207/mirai_http_python)  
不知道改了多少, 目前版本的 mirai-console 能用就是了  
啰唆一句, 是 AGPL

DEMO:

```python
#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from pymirai import BOT

class info:
    host = "http://localhost:8080"
    botqq = bot的QQ
    botkey = "mirai api http 的key "
    adminqq = 你的QQ


##############################################################################


def 群组消息(bot, msg):

    群号 = msg['sender']['group']['id']
    def 说(消息):
        机器人.发消息给群(群号, [{"type": "Plain", "text": 消息}, ])

    if (msg['messageChain'][1]['type'] == "Plain"):
        if (msg['messageChain'][1]['text']=="你好"):
            说("你好")


##############################################################################


def 好友事件(bot, msg):
    usr_id = msg['sender']['id']
    if usr_id == info.adminqq:
        机器人.发消息给好友(usr_id, [{"type": "Plain", "text": "你是管理员"},])
    else:
        机器人.发消息给好友(usr_id,[{"type": "Plain", "text": "你是好友"}, ])


##############################################################################
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
