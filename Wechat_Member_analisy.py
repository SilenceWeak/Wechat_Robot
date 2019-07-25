import itchat
import pandas as pd
import json
import os

#获取所有群聊列表
def get_roomlist():
    roomlist = itchat.get_chatrooms()
    return roomlist
#获取指定群聊信息
def get_roommsg(roomName):
    itchat.dump_login_status()#导出设置
    myroom = itchat.search_chatrooms(name=roomName)
    return myroom
#获取性别统计
def get_sex(df_friends):
    sex = df_friends['NickName'] + df_friends['Sex'].replace({1:'男',2:'女',0:'未知'})
    return sex
#将每个群聊中群成员的头像保存进文本文件中
def saveChatroomMemHeadimg(df_friends,roomName):
    usernmaeList = pd.DataFrame(df_friends,columns = ['NickName','HeadImgUrl'])
    path = "E:\\visual studio docu\\WeChat-Robot\\userIfo\\" + roomName
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
    for row in usernmaeList.itertuples():
        filename = "userIfo/"+roomName+'/'+getattr(row, 'NickName') +'.jpg'
        print(getattr(row,'HeadImgUrl'))
        #img = itchat.get_head_img(userName=getattr(row, 'UserName'))
        '''with open(filename,'wb') as file:
            file.write(img)'''
#每个群聊中群成员信息文本流打印
def saveChatroomList(df_friends_out,roomName):
    filename = "chatroom_memlist/" + roomName + ".dat"
    with open(filename,'w',encoding='utf-8') as f:
        f.write(df_friends_out)
#main函数
def main():
    itchat.auto_login(hotReload = True)
    roomlist = get_roomlist()
    print("信息存储开始！")
    for list in roomlist:
        userName = list['UserName']
        gsq = itchat.update_chatroom(userName,detailedMember=True)
        df_friends = pd.DataFrame(gsq['MemberList'])
        #df_friends['Sex'] = df_friends['Sex'].replace({1:'男',2:'女',0:'未知'})
        newdf = pd.DataFrame(df_friends,columns = ['NickName','Sex','Signature'])
        out = newdf.to_json(orient = 'records',force_ascii = False,lines = True,)
        #saveChatroomList(out,list['NickName'])
        saveChatroomMemHeadimg(df_friends,list['NickName'])
        df_string = json.dumps(out)
    print("信息存储完成！")

if __name__ =='__main__':
    main()