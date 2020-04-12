#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import time
import traceback
import threading


class BOT:
    群事件="GroupMessage"
    好友事件="FriendMessage"
    def __init__(self, url, qq, authKey):
        self.qq = qq
        self.sessionKey = None
        self.url = url
        self.authKey = authKey
        self.connecterrmsg = None
        self.wait = True


    def 登录(self,密码):
        """
        登不上的。\n
        请 在 后 台 使 用 该 指 令
        """
        req = {
            "authKey": self.authKey,
            "name": "login",
            "args": [self.qq, 密码]
            }
        
        res = requests.post(url=self.url+"/command/send",
                            json=req, timeout=10)
        print(res.text)
        return res
        
    def 连接(self):
        self.断开()
        print("request:", "auth", {"authKey": self.authKey})
        res = requests.post(url=self.url+"/auth",
                            json={"authKey": self.authKey}, timeout=10)
        try:
            res = res.json()
        except:
            return False
        print("response:", "auth", res)
        if res['code'] != 0:
            connecterrmsg = "error log:" + "get session failed"
            print("error log:", "get session failed")
        else:
            print("request:", "verify", {
                  "sessionKey": res['session'], "qq": self.qq})
            ress = requests.post(
                url=self.url+"/verify", json={"sessionKey": res['session'], "qq": self.qq}, timeout=10)
            print("response:", "verify", ress.text)
            ress = ress.json()
            if ress['code'] == 0:
                self.sessionKey = res['session']
                return True
            else:
                connecterrmsg = "error log:" + "verify session failed"
                print("error log:", "verify session failed")
        return False

    def 断开(self):
        if self.sessionKey != None:
            print("request:", "release", {
                  "sessionKey": self.sessionKey, "qq": self.qq})
            res = requests.post(
                url=self.url+"/release", json={"sessionKey": self.sessionKey, "qq": self.qq}, timeout=10)
            print("response:", "release", res.text)
            self.sessionKey = None

    def __del__(self):
        self.断开()

    def 发消息给好友(self, target, messageChain, quote=None):
        req = {"sessionKey": self.sessionKey,
               "target": target, "messageChain": messageChain}
        if quote != None:
            req["quote"] = quote
        #print("request:", "sendFriendMessage", req)
        res = requests.post(
            url=self.url+"/sendFriendMessage", json=req, timeout=10)
        ret = res.content
        #print("response:", "sendFriendMessage", res.text)
        return ret

    def 发消息给群(self, target, messageChain, quote=None):
        req = {"sessionKey": self.sessionKey,
               "target": target, "messageChain": messageChain}
        if quote != None:
            req["quote"] = quote
        #print("request:", "sendGroupMessage", req)
        res = requests.post(
            url=self.url+"/sendGroupMessage", json=req, timeout=10)
        ret = res.content
        #print("response:", "sendGroupMessage", str(ret))
        return ret

    def 发图片(self, urls, target=None, qq=None, group=None):
        req = {"sessionKey": self.sessionKey, "urls": urls}
        if target != None:
            req["target"] = target
        if qq != None:
            req["qq"] = qq
        if group != None:
            req["group"] = group
        #print("request:", "sendImageMessage", req)
        res = requests.post(
            url=self.url+"/sendImageMessage", json=req, timeout=10)
        ret = res.content
        #print("response:", "sendImageMessage", str(ret))
        return ret

    def 上传图像(self, type, img):
        print("request:", "uploadImage", {"type": type, "img": "..."})
        res = requests.post(self.url+"/uploadImage", data={
                            "sessionKey": self.sessionKey, 'type': type}, files={"img": img}, timeout=10)
        ret = res.text
        ret = json.loads(ret)["imageId"]
        print("response:", "uploadImage", str(ret))
        return ret

    def 撤回(self, target):
        req = {"sessionKey": self.sessionKey, "target": target}
        print("request:", "recall", req)
        res = requests.post(url=self.url+"/recall", json=req, timeout=10)
        ret = res.content
        print("response:", "recall", str(ret))
        return ret

    def 好友列表(self):
        req = "/friendList?sessionKey="+self.sessionKey
        print("request:", "friendList", req)
        res = requests.get(self.url + req, timeout=10)
        ret = res.content
        print("response:", "friendList", str(ret))
        return ret

    def 群列表(self):
        req = "/groupList?sessionKey="+self.sessionKey
        print("request:", "groupList", req)
        res = requests.get(self.url + req, timeout=10)
        ret = res.content
        print("response:", "groupList", str(ret))
        return ret

    def memberList(self, target):
        req = "/memberList?sessionKey=" + \
            self.sessionKey+"&target=" + str(target)
        print("request:", "memberList", req)
        res = requests.get(self.url + req, timeout=10)
        ret = res.content
        print("response:", "memberList", str(ret))
        return ret

    def 全员禁言(self, target):
        req = {"sessionKey": self.sessionKey, "target": target}
        print("request:", "muteAll", req)
        res = requests.post(url=self.url+"/muteAll", json=req, timeout=10)
        ret = res.content
        print("response:", "muteAll", str(ret))
        return ret

    def 取消全员禁言(self, target):
        req = {"sessionKey": self.sessionKey, "target": target}
        print("request:", "unmuteAll", req)
        res = requests.post(url=self.url+"/unmuteAll", json=req, timeout=10)
        ret = res.content
        print("response:", "unmuteAll", str(ret))
        return ret

    def 禁言(self, target, memberId, time=0):
        req = {
            "sessionKey": self.sessionKey,
            "target": target,
            "memberId": memberId,
            "time": time
        }
        print("request:", "mute", req)
        res = requests.post(url=self.url+"/mute", json=req, timeout=10)
        ret = res.content
        print("response:", "mute", str(ret))
        return ret

    def 取消禁言(self, target, memberId):
        req = {
            "sessionKey": self.sessionKey,
            "target": target,
            "memberId": memberId,
        }
        print("request:", "unmute", req)
        res = requests.post(url=self.url+"/unmute", json=req, timeout=10)
        ret = res.content
        print("response:", "unmute", str(ret))
        return ret

    def 踢(self, target, memberId, msg=None):
        req = {
            "sessionKey": self.sessionKey,
            "target": target,
            "memberId": memberId,
        }
        if msg != None:
            req["msg"] = msg
        print("request:", "kick", req)
        res = requests.post(url=self.url+"/kick", json=req, timeout=10)
        ret = res.content
        print("response:", "kick", str(ret))
        return ret

    def 群信息获取(self, target):
        req = "/groupConfig?sessionKey=" + \
            self.sessionKey+"&target=" + str(target)
        print("request:", "groupConfig", req)
        res = requests.get(self.url + req, timeout=10)
        ret = res.content
        print("response:", "groupConfig", str(ret))
        return ret

    def 成员信息获取(self, target, memberId):
        req = "/memberInfo?sessionKey="+self.sessionKey + \
            "&target=" + str(target)+"&memberId=" + str(memberId)
        print("request:", "memberInfo", req)
        res = requests.get(self.url + req, timeout=10)
        ret = res.content
        print("response:", "memberInfo", str(ret))
        return ret

    def 拉消息(self, count=10):
        res = requests.get(url=self.url+"/fetchLatestMessage?sessionKey=" +
                           self.sessionKey+"&count="+str(count), timeout=10)
        ret = res.content
        return ret

    def 等(self, timescale=0.5):
        class 线程 (threading.Thread):
            def __init__(self, funcvec, bot, msg):
                threading.Thread.__init__(self)
                self.funcvec = funcvec
                self.bot = bot
                self.msg = msg

            def run(self):
                for func in self.funcvec:
                    try:
                        func(self.bot, self.msg)
                    except:
                        traceback.print_exc()
        self.wait = True
        while self.wait:
            msgs = []
            try:
                msgs = json.loads(self.拉消息())["data"]
                # print(msgs)
            except:
                pass
            #if len(msgs): print(msgs)
            # if type(msgs["data"]) == dict:  #旧版
            #    msgs=[]
            for msg in msgs:
                # print("message:",msg)
                msgtype = msg['type']
                if msgtype != "GroupMessage":
                    print("message:", msg)
                f = None
                try:
                    f = getattr(self, msgtype)
                except:
                    pass
                try:
                    if f != None:
                        # f(self,msg)
                        线程一 = 线程(f, self, msg)
                        线程一.start()
                except:
                    traceback.print_exc()
            time.sleep(timescale)

    def 不等了(self):
        self.wait = False

    def 新增事件(self, msgtype, func):
        if(hasattr(self, msgtype)):
            getattr(self, msgtype).append(func)
        else:
            setattr(self, msgtype, [])
            getattr(self, msgtype).append(func)
