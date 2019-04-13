# -*- coding:utf-8 -*-
import pprint

import itchat
import re

import jieba

import blacktale_predict
from itchat.content import *


# 检测work
def check_summary(msg):
    word_list = jieba.cut(msg, cut_all=True)
    www = list(word_list)
    # print("/".join(www))

    keywords = []
    for line in open("data/keyword.txt", "r"):
        keywords.append(line.strip().split())

    result = 1
    for i in keywords:
        flag = 0
        for word in www:
            if word in i:
                flag = 1
        if flag == 0:
            result = 0
            break
    return result == 1



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

jieba.load_userdict("data/keyword_jieba.txt")


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

    matchAsk = False
    matchNo = False
    matchWuguan = False
    matchZongJie = False

    if msg['Text'].startswith('总结：') or msg['Text'].startswith('总结:'):
        matchZongJie = check_summary(msg['Text'])
    else:
        possibilities = blacktale_predict.predict(msg['Text'])
        predict_ans = possibilities.index(max(possibilities))

        matchAsk = predict_ans == 0
        matchNo = predict_ans == 1
        matchWuguan = predict_ans == 2

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
        success = check_summary(msg['Text'])
        print(msg['Text'], '总结成功' if success else '总结失败')
        if success:
            itchat.send('「 %s: %s 」\n- - - - - - - - - - - - - - -\n总结成功，太流批啦！' % (
                user_nickname, msg['Text']), group_id)
            f = 'img/%s' % (zongjieImgDict.get('1'))
            itchat.send_image(f, group_id)
            print('发送图片' + f)
        else:
            zongJieInt = zongJieInt + 1
            zongjieDict[user_nickname] = zongJieInt
            print('zongjieDict+1')
            print(zongjieDict)
            itchat.send('「 %s: %s 」\n- - - - - - - - - - - - - - -\n总结错误…… T_T' % (
                user_nickname, msg['Text']), group_id)
            f = 'img/%s' % (zongjieImgDict.get('2'))
            itchat.send_image(f, group_id)
            print('发送图片' + f)

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
