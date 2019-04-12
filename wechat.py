# -*- coding:utf-8 -*-
import pprint

import itchat
import re
import blacktale_predict
from itchat.content import *


# 检测work
def checkAsk(msg):
    msg1 = '是不是'
    msg2 = '吗'
    return re.search(msg1.encode('gbk'), msg.encode('gbk')) or re.search(msg2.encode('gbk'), msg.encode('gbk'))


def checkZongJie(msg):
    msg100 = '总结'
    return re.search(msg100.encode('gbk'), msg.encode('gbk'))


def checkNo(msg):
    msg3 = '否定回答'
    return re.search(msg3.encode('gbk'), msg.encode('gbk'))


def checkWuguan(msg):
    msg3 = '无关紧要'
    return re.search(msg3.encode('gbk'), msg.encode('gbk'))


yesDict = {}
yesTextDict = {'1': '乖乖，你可真是个鬼才，总是能观察到别人看不到的细节，恭喜你获得鬼才称号', '2': '你是爱因斯坦吗，这都被你发现了，恭喜你获得天才称号',
               '3': '请问你是二郎神吗，可以从多角度观察事物，二郎神称号非你莫属', '4': '难道你就是消失多年的工藤新一吗，恭喜你获得名侦探柯南称号',
               '5': '问了五次有效的问题可以召唤神龙，恭喜你成为驭龙勇士'}
yesImgDict = {'1': 'img1', '2': 'img2', '3': 'img3', '4': 'img4', '5': 'img5'}

noDict = {}
noTextDict = {'1': '总是抓不到重点，难道你就是毛利小五郎吗，恭喜你获得毛利小五郎称号',
              '2': '问几次错误的问题可召唤不了真正的神龙，恭喜你成为驭虫勇士',
              '3': '走偏了这么多次，你不觉得羞愧吗，恭喜你获得没脸见人称号',
              '4': '能问这么多次，我真的佛了'}
noImgDict = {'1': 'noimg2',
             '2': 'noimg4',
             '3': 'noimg8',
             '4': 'noimg16'}

zongjieDict = {}
zongjieTextDict = {'1': '总结成功',
                   '2': '总结失败',
                   '3': '总结成功',
                   '4': '总结失败'}
zongjieImgDict = {'1': 'success.png',
                  '2': 'fail.gif',
                  '3': 'success.png',
                  '4': 'fail.gif'}

wuguanDict = {}
wuguanTextDict = {'1': '你可真会瞎问，恭喜你独眼龙称号',
                  '2': '请问你是李青吗，恭喜你获得盲僧称号',
                  '3': '问这么多次无关紧要的问题可召唤不了神龙，恭喜你获得驭蛇勇士称号',
                  '4': '老是瞎JB问，恭喜你获得XJBW称号'}
wuguanImgDict = {'1': 'zongjie1',
                 '2': 'zongjie2',
                 '3': 'zongjie3',
                 '4': 'zongjie4'}


@itchat.msg_register(TEXT, isGroupChat=True)
def getNoteGroup(msg):
    # 确定群聊 msg['User'] 为聊天信息
    if msg['User']['NickName'] != '黑马测试消息专用群':
        return
    group_id = msg['User']['UserName']

    if msg['ActualNickName'] != '':
        user_nickname = msg['ActualNickName']
    else:
        user_nickname = "default_name==="
    print('user_nickname: ' + user_nickname)

    # yes次数
    if user_nickname in yesDict:
        print('yesDict已经有')
        print(yesDict)
    else:
        yesDict[user_nickname] = 0
        print('yesDict初始化')
        print(yesDict)
    yesInt = yesDict.get(user_nickname)

    # no次数
    if user_nickname in noDict:
        print('noDict已经有')
        print(noDict)
    else:
        noDict[user_nickname] = 0
        print('noDict初始化')
        print(noDict)
    noInt = noDict.get(user_nickname)

    # zongjie次数
    if user_nickname in zongjieDict:
        print('zongjieDict已经有')
        print(zongjieDict)
    else:
        zongjieDict[user_nickname] = 0
        print('zongjieDict初始化')
        print(zongjieDict)

    zongJieInt = zongjieDict.get(user_nickname)

    # wuguan次数
    if user_nickname in wuguanDict:
        print('zongjieDict已经有')
        print(wuguanDict)
    else:
        wuguanDict[user_nickname] = 0
        print('zongjieDict初始化')
        print(wuguanDict)

    wuguanInt = wuguanDict.get(user_nickname)

    print('receive:' + msg['Text'])
    print('from:' + user_nickname)
    pprint.pprint(msg)
    print('receive:' + msg['Text'])

    possibilities = blacktale_predict.predict_outside(msg['Text'])
    predict_ans = possibilities.index(max(possibilities))

    matchAsk = predict_ans == 0
    matchNo = predict_ans == 1
    matchWuguan = predict_ans == 2
    matchZongJie = False  # checkZongJie(msg['Text'])

    if matchAsk:
        print(msg['Text'] + 'matchAsk')
        yesInt = yesInt + 1
        yesDict[user_nickname] = yesInt
        itchat.send('「 %s: %s 」\n- - - - - - - - - - - - - - -\n是,这是您第%s次获得肯定回答' % (
            user_nickname, msg['Text'], yesInt), group_id)
        print('yesDict+1')
        print(yesDict)
        if yesImgDict.get(str(yesInt)):
            f = 'img/%s.png' % (yesImgDict.get(str(yesInt)))
            itchat.send_image(f, group_id)
            print('发送图片' + f)
        if yesTextDict.get(str(yesInt)):
            itchat.send(yesTextDict.get(str(yesInt)), group_id)

    if matchNo:
        print(msg['Text'] + 'matchNo')
        noInt = noInt + 1
        noDict[user_nickname] = noInt
        itchat.send('「 %s: %s 」\n- - - - - - - - - - - - - - -\n否,这是您第%s次获得否定回答' % (
            user_nickname, msg['Text'], noInt), group_id)
        print('noInt+1')
        print(noDict)
        #            if noInt == 2 or noInt == 4 or noInt == 8 or noInt == 16 :
        #                f = 'img/noimg%s.png' % (yesInt)
        #            itchat.send_image(f, group_id)
        #            print('发送图片'+f)
        #            f="img/img1.png" #图片地址
        #            itchat.send_image(f, group_id)
        #            print('发送图片'+f)
        if noImgDict.get(str(noInt)):
            f = 'img/%s.png' % (noImgDict.get(str(noInt)))
            itchat.send_image(f, group_id)
            print('发送图片' + f)
        if noTextDict.get(str(noInt)):
            itchat.send(noTextDict.get(str(noInt)), group_id)

    if matchZongJie:
        print(msg['Text'] + 'matchZongJie')
        zongJieInt = zongJieInt + 1
        zongjieDict[user_nickname] = zongJieInt
        print('zongjieDict+1')
        print(zongjieDict)
        itchat.send('「 %s: %s 」\n- - - - - - - - - - - - - - -\n总结错误，这是您第%s次总结' % (
            user_nickname, msg['Text'], zongJieInt), group_id)
        if zongjieImgDict.get(str(zongJieInt)):
            f = 'img/%s' % (zongjieImgDict.get(str(zongJieInt)))
            itchat.send_image(f, group_id)
            print('发送图片' + f)
        if zongjieTextDict.get(str(zongJieInt)):
            itchat.send(zongjieTextDict.get(str(zongJieInt)), group_id)
    # 无关紧要
    if matchWuguan:
        print(msg['Text'] + 'matchWuguan')
        wuguanInt = wuguanInt + 1
        wuguanDict[user_nickname] = wuguanInt
        print('wuguanDict+1')
        print(wuguanDict)
        itchat.send('「 %s: %s 」\n- - - - - - - - - - - - - - -\n无关紧要，这是您第%s次问一些无关的问题' % (
            user_nickname, msg['Text'], wuguanInt), group_id)
        if wuguanImgDict.get(str(wuguanInt)):
            f = 'img/%s.png' % (wuguanImgDict.get(str(wuguanInt)))
            itchat.send_image(f, group_id)
            print('发送图片' + f)
        if wuguanTextDict.get(str(wuguanInt)):
            itchat.send(wuguanTextDict.get(str(wuguanInt)), group_id)


def main():
    # 登录
    itchat.auto_login(hotReload=True)
    # 运行监控
    itchat.run()
    # 退出登录
    itchat.logout()


if __name__ == '__main__':
    main()
