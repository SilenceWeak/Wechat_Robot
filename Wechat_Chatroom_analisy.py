import json
import urllib,sys,ssl
import urllib.request
import urllib3
import requests
import itchat
import os

#获取所有群聊列表
def get_roomlist():
    roomlist = itchat.get_chatrooms()
    return roomlist
#与百度文本分析AI进行交互
def response_BaiduAi(msg):
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=9QsV6s5dR6fMXfPr0UUxViy0&client_secret=vHblzySvFD9UzLxmlfhGXrpzL6qbbSzL'
    request1 = urllib.request.Request(host)
    request1.add_header('Content-Type', 'application/json; charset=UTF-8')
    response1 = urllib.request.urlopen(request1)
    content = response1.read()
    content_str = str(content,encoding = "utf-8")
    content_json = json.loads(content_str,encoding="utf-8")
    access_token = content_json['access_token']
    #api地址
    http = urllib3.PoolManager()
    url = 'https://aip.baidubce.com/rest/2.0/antispam/v2/spam?access_token=' + access_token
    data = "content="+msg
    encode_data=data.encode("utf-8")
    headers = {'Content-Type':'application/x-www-form-urlencoded'}
    request2 = urllib.request.Request(url,encode_data)
    request2.add_header('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
    response2 = urllib.request.urlopen(request2)
    content2 = response2.read()
    content2_str = str(content2,encoding = "utf-8")
    print(content2_str)
    #选取置信度最高的进行输出

#与百度文章分析AI进行交互
def response_BaiduAi_kind(msg,text_title):
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=tsDccnjv29vGQ7y6upDQhN0p&client_secret=bjIPklCbd2iKRti4ACGq5SdlmCELO1PT'
    request1 = urllib.request.Request(host)
    request1.add_header('Content-Type', 'application/json; charset=UTF-8')
    response1 = urllib.request.urlopen(request1)
    content = response1.read()
    content_str = str(content,encoding = "utf-8")
    content_json = json.loads(content_str,encoding="utf-8")
    access_token = content_json['access_token']

    #文章分类接口
    http = urllib3.PoolManager()
    url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/topic?access_token=' + access_token
    data = {
                "title":text_title,
                "content":msg
           }
    encode_data = json.dumps(data,ensure_ascii= False).encode("GBK")
    headers = {'Content-Type':'applicx-www-form-urlencodedation/'}
    request2 = urllib.request.Request(url,encode_data)
    request2.add_header('Content-Type','application/json; charset=GBK')
    response2 = urllib.request.urlopen(request2)
    content2 = response2.read()
    content2_str = str(content2,encoding = "GBK")
    print(content2_str)
    content2_dic = json.loads(content2_str,encoding="GBK")
    level1 = content2_dic['item']['lv1_tag_list'][0]['tag']
    #如果二级分类中不存在元素便只返回一级分类
    if(content2_dic['item']['lv2_tag_list'] == []):
        return level1
    else:
        #存在二级分类则返回二级分类
        level2 = content2_dic['item']['lv2_tag_list'][0]['tag']
        return level2

#从文件中读取text文件，然后使用百度自然语言分类AI进行分类
def Baidu_read_msg(NickName):
    filename1 = "text_of_chatroom/"+NickName+".dat"
    with open(filename1,'a+') as f:
        read = f.read()
        if read == "":
            read = NickName
        outcome = response_BaiduAi_kind(read,NickName)
    '''path = "E:\\visual studio docu\\WeChat-Robot\\senIfo\\" + NickName
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)'''
    filename2 = "senIfo/label_of_chatroom.json"
    outcome_json =  {
                        "ChatroomName":NickName,
                        "labels":outcome
                    }
    with open(filename2,'a') as f:
        f.write("{\n\t\"ChatroomName\":" + NickName +",\n\t\"labels\":"+outcome+"\n}\n")

if __name__=='__main__':
    itchat.auto_login(hotReload=True)
    with open("senIfo/label_of_chatroom.json",'w') as f:
        pass
    roomlist = get_roomlist()
    print("信息存储开始！")
    for list in roomlist:
        userName = list['NickName']
        Baidu_read_msg(userName)
        input()
