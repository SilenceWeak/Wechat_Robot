import itchat,time
import requests
from itchat.content import *
import os
import pandas as pd
import matplotlib.pyplot as plot
import numpy
from wordcloud import WordCloud
from pyecharts.charts import Bar , Page
import jieba
import sys
import importlib
from matplotlib.font_manager import _rebuild
import threading
import _thread
import json
import urllib,sys,ssl
import urllib.request
import urllib3
import requests
import datetime
import re




importlib.reload(sys)
KEY = 'dac1ec679dde4e84a4920ba40c3ee944'
#与图灵机器人进行交互
def response_turing(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key' : KEY,
        'info' : msg,
        'userid' : 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl,data=data).json()
        return r.get('text')
    except:
        return
#将聊天信息存储进text文件中，方便百度AI接口直接调用
def save_msg(msg, NickName):
    filename = "text_of_chatroom/"+NickName+".dat"
    with open(filename,'a',encoding='utf-8') as f:
        if((msg.find(',') == -1) and (msg.find('。') == -1) and (msg.find('？') == -1) and (msg.find('！') == -1) and (msg.find('、') == -1)):
            f.write(msg+",")
        else:
            f.write(msg)

#聊天信息文件备份
def save_msg_contact(msg,NickName):
    dayTime = datetime.datetime.now().strftime('%Y.%m.%d')
    theTime = datetime.datetime.now().strftime('%H:%M:%S')
    msg = theTime + '\n' + msg + '\n'
    path = "E:\\visual studio docu\\WeChat-Robot\\content_text\\" + NickName
    filename = "content_text/"+NickName+"/"+ dayTime + ".dat"
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    with open(filename,'a',encoding='utf-8') as f:
        f.write(msg)
#提取URL
def FindURL(string):
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',string)
    return url
#提取domin
def FindDomin(string):
    domin = re.findall('http[s]://.*?\.com|http[s]://.*?\.cn|http[s]://.*?\.net',string)
    return domin
#提取ip地址
def FindIP(string):
    ip = re.findall('(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}',string)
    return ip
#存储群聊中发出的URL、ip地址及其发出者的信息
def save_URL_IP_Chatroom(string,msg):
    dayTime = datetime.datetime.now().strftime('%Y.%m.%d')
    theTime = datetime.datetime.now().strftime('%H:%M:%S')
    url = ','.join(FindURL(string))
    domin = ','.join(FindDomin(string))
    ip = ','.join(FindIP(string))
    if url == "" and ip == "" and domin == "":
        return
    else:
        path = "E:\\visual studio docu\\WeChat-Robot\\senIfo\\" + msg.User["NickName"]
        filename = "senIfo/"+msg.User["NickName"]+"/"+dayTime + ".dat"
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
        save_url = theTime+'\n'+ msg.User["NickName"] + "群成员——\n微信注册码:"+msg['FromUserName'] +"\n微信昵称:"+ msg["ActualNickName"] + ': ' + url +'\n'
        save_domin = theTime+'\n'+ msg.User["NickName"] + "群成员——\n微信注册码:"+msg['FromUserName'] +"\n微信昵称:"+ msg["ActualNickName"] + ': ' + domin +'\n'
        save_ip = theTime+'\n'+ msg.User["NickName"] + "群成员——\n微信注册码:"+msg['FromUserName'] +"\n微信昵称:"+ msg["ActualNickName"] + ': ' + ip +'\n'
        with open(filename,'a',encoding='utf-8') as f:
            if url != "":
                f.write(save_url)
            if domin != "":
                f.write(save_domin)
            if ip != "":
                f.write(save_ip)
#微信消息接收模块
'''@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    contact_text = msg.User['NickName']+":"+msg.text
    #defaulReply是当Key出现问题的时候仍然可以回复默认回复消息
    print(contact_text)
    defaultReply = msg.text
    reply = response_turing(msg.text)
    contact_reply = "第三杯星光: " + reply or defaultReply
    print(reply or defaultReply +'\n')
    #将数据以文本形式保存进.dat文件中以供百度AI文章分析集中调用
    save_msg(msg.text,msg.User["NickName"])
    save_msg(reply or defaultReply,msg.User["NickName"])
    #将数据以文本形式保存进.dat以供查阅聊天记录
    save_msg_contact(contact_text,msg.User["NickName"])
    save_msg_contact(contact_reply,msg.User["NickName"])
    return reply or defaultReply
#回复群消息模块'''
@itchat.msg_register(itchat.content.TEXT,isGroupChat=True)
def group_reply(msg):
    #群聊消息时只回复被@之后的内容
    if msg.User["NickName"] != "":
        text = msg.text
        if(text.find("@第三杯星光") != -1) :
            if(len(msg.text) > 7):
                text = text[7:]
            else:
                text = ""
        else:
            pass
        contact_text = "群聊" + msg.User["NickName"] +"，"+msg["ActualNickName"]+ "：" + text
        print(contact_text)
        save_msg_contact(contact_text,msg.User["NickName"])
        save_msg(text,msg.User["NickName"])
        save_URL_IP_Chatroom(text,msg)
        if(msg.isAt):
            defaultReply = text
            reply = response_turing(text)
            contact_reply = "第三杯星光: " + reply or defaultReply
            save_msg_contact(contact_reply,msg.User["NickName"])
            save_msg(reply or defaultReply,msg.User["NickName"])
            print(contact_reply+'\n')
            return reply or defaultReply
    else:
        pass

if __name__=='__main__':
    itchat.auto_login(hotReload=True)
    itchat.run()
